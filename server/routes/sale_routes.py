"""sale_routes.py
This module defines routes for handling sales transactions in the application.
It includes endpoints to retrieve all sales and create a new sale with items.
"""
from flask import Blueprint, request, jsonify
from server.models import db, Sale, SaleItem, Product

# Blueprint for sale-related routes
sale_bp = Blueprint('sale_bp', __name__)

@sale_bp.route('/sales', methods=['GET'])
def get_sales():
    """
    Retrieve all sales from the database.
    Returns a list of sales, each including its items and customer info.
    """
    sales = Sale.query.all()
    return jsonify([s.to_dict() for s in sales])

@sale_bp.route('/sales', methods=['POST'])
def create_sale():
    """
    Create a new sale (transaction).
    Steps:
    1. Receive customer_id and items (product_id, quantity) from request JSON.
    2. Validate that each product exists and has enough stock.
    3. If any product is invalid or stock is insufficient, rollback and return error.
    4. Create a Sale and related SaleItem records.
    5. Deduct sold quantity from product stock.
    6. Calculate and set the total sale amount.
    7. Commit all changes in a single transaction.
    8. Return the new sale as JSON.
    """
    data = request.get_json()
    customer_id = data.get('customer_id')
    items = data.get('items', [])
    total = 0
    sale = Sale(customer_id=customer_id, total=0)
    db.session.add(sale)
    db.session.flush()  # Get sale.id
    for item in items:
        product = Product.query.get(item['product_id'])
        if not product or product.stock < item['quantity']:
            db.session.rollback()
            return jsonify({'error': 'Invalid product or insufficient stock'}), 400
        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=item['quantity'],
            price=product.price
        )
        product.stock -= item['quantity']
        total += product.price * item['quantity']
        db.session.add(sale_item)
    sale.total = total
    db.session.commit()
    return jsonify(sale.to_dict()), 201
