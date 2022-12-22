import datetime

from slugify import slugify
from sqlalchemy.exc import IntegrityError

from app import db

cart_product = db.Table('cart_product',
                        db.Column('cart_id', db.Integer, db.ForeignKey('shopping_cart.id'), primary_key=True),
                        db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
                        )


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    posts = db.relationship("PostProduct", back_populates="product_parent", lazy=True, cascade="all, delete-orphan",
                            order_by="PostProduct.created")
    carts = db.relationship("ShoppingCart", secondary=cart_product, back_populates="products")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Product.query.all()

    @staticmethod
    def get_by_id(id):
        return Product.query.filter_by(id=id).first()

    @staticmethod
    def commit():
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class PostProduct(db.Model):
    __tablename__ = 'post_product'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    title_slug = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    image_name = db.Column(db.String, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product_parent = db.relationship("Product", back_populates="posts")
    comments = db.relationship("CommentProduct", back_populates="post_parent",
                               lazy=True, cascade="all, delete-orphan", order_by="CommentProduct.created")

    def __repr__(self):
        return f'<Post> {self.title}'

    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.title_slug:
            self.title_slug = slugify(self.title)

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                db.session.rollback()  # Añade esta línea
                db.session.add(self)  # y esta
                count += 1
                self.title_slug = f'{slugify(self.title)}-{count}'

    @staticmethod
    def get_by_slug(slug):
        return PostProduct.query.filter_by(title_slug=slug).first()

    @staticmethod
    def get_all():
        return PostProduct.query.all()

    @staticmethod
    def get_by_id(id):
        return PostProduct.query.filter_by(id=id).first()

    @staticmethod
    def get_by_product(product_id):
        return PostProduct.query.filter_by(product_id=product_id).all()

    @staticmethod
    def get_by(parameters):
        return PostProduct.query.filter_by(**parameters).first()

    @staticmethod
    def commit():
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return PostProduct.query.get(id)

    @staticmethod
    def all_paginated(page=1, per_page=20):
        return PostProduct.query.order_by(PostProduct.created.asc()). \
            paginate(page=page, per_page=per_page, error_out=False)


class CommentProduct(db.Model):
    __tablename__ = 'comment_product'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey("post_product.id"))
    post_parent = db.relationship("PostProduct", back_populates="comments")
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return f'<Comment {self.content}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_post_id(post_id):
        return CommentProduct.query.filter_by(post_id=post_id).all()

    @staticmethod
    def get_by(parameters):
        return CommentProduct.query.filter_by(**parameters).first()

    @staticmethod
    def get_by_id(id):
        return CommentProduct.query.get(id)

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def get_all():
        return CommentProduct.query.all()


class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'

    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False, default=0)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    products = db.relationship("Product", secondary=cart_product, back_populates="carts")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
