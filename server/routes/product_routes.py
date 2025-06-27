from flask import Blueprint, request, jsonify
from server.models import db, Product

# Blueprint for product-related routes
product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    """
    Retrieve all products from the database.
    Returns a list of products as JSON.
    """
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])
@product_bp.route('/products', methods=['POST'])
def create_product():
    """
    Create a new product.
    Validates input data (name, price, stock).
    Returns the created product as JSON with status 201, or error messages with status 400.
    """
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

@product_bp.route('/products/<int:id>', methods=['GET'])
def get_product():
    """
    Retrieve a single product by its ID.
    Returns the product as JSON, or 404 if not found.
    """
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict())

@product_bp.route('/products/<int:id>', methods=['PUT'])
def update_product():
    """
    Update an existing product by its ID.
    Validates input data and updates fields if valid.
    Returns the updated product as JSON, or error messages with status 400/404.
    """
    product = Product.query.get()
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

@product_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product():
    """
    Delete a product by its ID.
    Returns 204 on success, or 404 if not found.
    """
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return '', 204
