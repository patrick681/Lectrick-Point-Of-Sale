"""//seed.py
This module seeds the database with some test data."""
from random import randint
from faker import Faker

# Local imports
from app import app
from server.models import db, Product, Customer, User

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        db.drop_all()
        db.create_all()

        # Seed Products
        products = []
        for _ in range(10):
            p = Product(
                name=fake.unique.word().capitalize(),
                price=round(randint(100, 10000) / 100, 2),
                stock=randint(10, 100)
            )
            products.append(p)
            db.session.add(p)

        # Seed Customers
        customers = []
        for _ in range(5):
            c = Customer(
                name=fake.name(),
                email=fake.unique.email()
            )
            customers.append(c)
            db.session.add(c)

        # Seed Users (for authentication)
        user = User(username='admin', password_hash='admin')
        db.session.add(user)
        db.session.commit()
        print("Seeding complete!")
