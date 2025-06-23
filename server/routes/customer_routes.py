from flask import Blueprint, request, jsonify
from models import db, Customer

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers])

@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer = Customer(name=data['name'], email=data.get('email'))
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201
