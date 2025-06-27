from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import re

from server.models import Product, Customer, User
from server.config import db, migrate

app = Flask(__name__)
CORS(app)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/app.db"
app.config['JWT_SECRET_KEY'] = 'replace-this-with-a-secure-random-key'

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

# Password validation helper
def is_password_valid(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[^A-Za-z0-9]', password)
    )

# JWT Auth routes
@app.route("/api/users/register", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 400

    if not is_password_valid(password):
        return jsonify({"error": "Password does not meet requirements"}), 400

    user = User(username=username, password_hash=password)  # NOTE: hash in production
    db.session.add(user)
    db.session.commit()

    return jsonify({"success": True}), 201

@app.route("/api/users/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or user.password_hash != password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify(access_token=token), 200

@app.route("/api/me", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user.to_dict())

@app.route("/api/users/check-username")
def check_username():
    username = request.args.get("username", "")
    available = not User.query.filter_by(username=username).first()
    return jsonify({"available": available})

# --- Product routes ---
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')
    errors = {}

    if not name or not isinstance(name, str):
        errors['name'] = 'Name is required and must be a string.'
    if price is None or not isinstance(price, (int, float)) or price < 0:
        errors['price'] = 'Price must be a non-negative number.'
    if stock is None or not isinstance(stock, int) or stock < 0:
        errors['stock'] = 'Stock must be a non-negative integer.'

    if errors:
        return jsonify({'errors': errors}), 400

    product = Product(name=name, price=price, stock=stock)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict())

@app.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json()
    name = data.get('name', product.name)
    price = data.get('price', product.price)
    stock = data.get('stock', product.stock)
    errors = {}

    if not isinstance(name, str):
        errors['name'] = 'Name must be a string.'
    if not isinstance(price, (int, float)) or price < 0:
        errors['price'] = 'Price must be a non-negative number.'
    if not isinstance(stock, int) or stock < 0:
        errors['stock'] = 'Stock must be a non-negative integer.'

    if errors:
        return jsonify({'errors': errors}), 400

    product.name = name
    product.price = price
    product.stock = stock
    db.session.commit()
    return jsonify(product.to_dict())

@app.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return '', 204

# --- Customer routes ---
@app.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers])

@app.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    data = request.get_json()
    customer = Customer(name=data['name'], email=data.get('email'))
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

if __name__ == "__main__":
    app.run(debug=True)

__all__ = [app, db, migrate, Product, Customer, User]
