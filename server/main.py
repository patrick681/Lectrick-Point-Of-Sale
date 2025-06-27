from flask import Flask, request, jsonify
import re
import logging
from server.models import Product, Customer
from server.config import db, migrate
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/app.db"
db.init_app(app)
migrate.init_app(app, db)
with app.app_context():
    db.create_all()


def is_password_valid(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[^A-Za-z0-9]', password)
    )

# --- Product routes directly in main.py ---

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON body'}), 400
    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')
    errors = {}
    if not name or not isinstance(name, str):
        errors['name'] = 'Name is required and must be a string.'
    if price is None or not isinstance(price, (int, float)) or price < 0:
        errors['price'] = 'Price is required and must be a non-negative number.'
    if stock is None or not isinstance(stock, int) or stock < 0:
        errors['stock'] = 'Stock is required and must be a non-negative integer.'
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
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON body'}), 400
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
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return '', 204

# --- End product routes ---

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

@app.route("/api/users/check-username")
def check_username():
    username = request.args.get("username", "")
    available = not any(u["username"] == username for u in users)
    return jsonify({"available": available})

@app.route("/api/users/register", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    if any(u["username"] == username for u in users):
        return jsonify({"error": "Username already taken"}), 400
    if not is_password_valid(password):
        return jsonify({"error": "Password does not meet requirements"}), 400
    users.append({"username": username, "password": password})
    return jsonify({"success": True})
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer = Customer(name=data['name'], email=data.get('email'))
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers])


if __name__ == "__main__":
    app.run(debug=True)
__all__ = [app, db, migrate, Product]