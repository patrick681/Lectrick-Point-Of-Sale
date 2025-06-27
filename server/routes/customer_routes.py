"""
Customer Routes Module

This module defines the routes for customer-related operations, including
retrieving and creating customers.
"""
from flask import Blueprint, request, jsonify
from server.models import db, Customer

# Blueprint for customer-related routes
customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/customers', methods=['GET'])
def get_customers():
    """
    Retrieve all customers from the database.
    Returns a list of customers as JSON.
    """
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers])

@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    """
    Create a new customer.
    Expects 'name' (required) and 'email' (optional) in the request JSON.
    Validates input data and returns the created customer as JSON with status 201,
    or error messages with status 400 if validation fails.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON body'}), 400
    name = data.get('name')
    email = data.get('email')
    errors = {}
    if not name or not isinstance(name, str):
        errors['name'] = 'Name is required and must be a string.'
    if email is not None and not isinstance(email, str):
        errors['email'] = 'Email must be a string.'
    if errors:
        return jsonify({'errors': errors}), 400
    customer = Customer(name=name, email=email)
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201
