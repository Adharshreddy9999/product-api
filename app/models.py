from datetime import datetime
from . import db
from sqlalchemy.orm import validates

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @validates('price')
    def validate_price(self, key, price):
        if not isinstance(price, (int, float, str)):
            raise ValueError("Price must be a number")
        price = float(price)
        if price < 0:
            raise ValueError("Price cannot be negative")
        return price

    @validates('stock')
    def validate_stock(self, key, stock):
        if not isinstance(stock, (int, str)):
            raise ValueError("Stock must be an integer")
        stock = int(stock)
        if stock < 0:
            raise ValueError("Stock cannot be negative")
        return stock

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if len(name) > 100:
            raise ValueError("Name cannot be longer than 100 characters")
        return name.strip()

    def __repr__(self):
        return f'<Product {self.name}>'
