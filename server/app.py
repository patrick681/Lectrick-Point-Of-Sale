#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
from routes.product_routes import product_bp
from routes.sale_routes import sale_bp
from routes.customer_routes import customer_bp

# Register Blueprints
app.register_blueprint(product_bp)
app.register_blueprint(sale_bp)
app.register_blueprint(customer_bp)


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

