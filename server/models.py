from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from server.config import db

# Product model: Represents an item for sale in the POS system.
class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)  # Product name
    price = db.Column(db.Float, nullable=False)  # Product price
    stock = db.Column(db.Integer, nullable=False)  # Units in stock

    # One-to-many: A product can have many sale items
    sale_items = db.relationship('SaleItem', back_populates='product', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }

# Customer model: Represents a customer who can make purchases.
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)  # Customer name
    email = db.Column(db.String, unique=True)    # Customer email (optional)

    # One-to-many: A customer can have many sales
    sales = db.relationship('Sale', back_populates='customer', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

# Sale model: Represents a transaction (purchase) made by a customer.
class Sale(db.Model, SerializerMixin):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))  # FK to Customer
    total = db.Column(db.Float, nullable=False)  # Total sale amount
    timestamp = db.Column(db.DateTime, server_default=db.func.now())    # Time of sale

    # Many-to-one: Each sale references one customer
    customer = db.relationship('Customer', back_populates='sales')
    # One-to-many: A sale can have many sale items
    items = db.relationship('SaleItem', back_populates='sale', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'total': self.total,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'items': [item.to_dict() for item in self.items]
        }

# SaleItem model: Represents a line item in a sale (product, quantity, price at sale time).
class SaleItem(db.Model, SerializerMixin):
    __tablename__ = 'sale_items'
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'))      # FK to Sale
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))# FK to Product
    quantity = db.Column(db.Integer, nullable=False)                # Quantity sold
    price = db.Column(db.Float, nullable=False)                     # Price at time of sale

    # Many-to-one: Each sale item references one sale and one product
    sale = db.relationship('Sale', back_populates='items')
    product = db.relationship('Product', back_populates='sale_items')

    def to_dict(self):
        return {
            'id': self.id,
            'sale_id': self.sale_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price,
            'product': self.product.to_dict() if self.product else None
        }

# User model: Represents a system user (for authentication/admin purposes).
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)  # Username
    password_hash = db.Column(db.String, nullable=False)          # Hashed password

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }