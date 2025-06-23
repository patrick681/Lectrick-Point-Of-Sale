from flask import Blueprint, request, jsonify
from models import db, Sale, SaleItem, Product, Customer

sale_bp = Blueprint('sale_bp', __name__)

@sale_bp.route('/sales', methods=['GET'])
def get_sales():
    sales = Sale.query.all()
    return jsonify([s.to_dict() for s in sales])

@sale_bp.route('/sales', methods=['POST'])
def create_sale():
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
