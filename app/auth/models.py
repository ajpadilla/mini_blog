from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.product.models import ShoppingCart


class UserCart(db.Model):
    __tablename__ = "user_cart"

    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id'), primary_key=True)
    shopping_cart_id = db.Column(db.Integer, db.ForeignKey('shopping_cart.id'), primary_key=True)
    status = db.Column(db.String(30), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    child = db.relationship("ShoppingCart")

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model, UserMixin):
    __tablename__ = 'blog_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    image_name = db.Column(db.String)
    carts = db.relationship("UserCart")

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()
