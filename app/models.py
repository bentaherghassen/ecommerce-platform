""" 
     User,Product,Order,OrderItem
"""
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False) # e.g., Male, Female
    phone_number = db.Column(db.BigInteger, nullable=False) 
    home_address = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.png")
    bio = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(60), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)
    
    def get_reset_token(self, expires_sec=3600): # Corrected and instance method
        s = Serializer(current_app.config['SECRET_KEY']) 
        return s.dumps({'user_id': self.id}).encode('utf-8')

    @staticmethod  # it's a static method
    def verify_reset_token(token): 
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.decode('utf-8'), max_age=3600)  # Max age is crucial
            user_id = data['user_id']
        except:
            return None
        return User.query.get(user_id)
def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50)) #food, pills, etc
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255)) #optional image    
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(100))  
    orders = db.relationship('OrderItem', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.name}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending') # Pending, Shipped, Delivered, Cancelled
    total_amount = db.Column(db.Float, nullable=False, default=0.0) #Calculated from order items
    shipping_address = db.Column(db.Text)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False) # Price at the time of order (might change later)

    def __repr__(self):
        return f'<OrderItem {self.id}>'
