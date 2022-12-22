import datetime
import logging
from flask import request, Blueprint, current_app, jsonify
from flask_restful import Api, Resource, reqparse
from sqlalchemy import select, desc

from app import db
from app.auth.models import User, UserCart
from app.product.exceptions import ProductNotFoundException, PostProductNotFoundException, \
    CommentProductNotFoundException
from app.product.helpers import make_user_cart
from app.product.schemas import ProductSchema, PostProductSchema, CommentProductSchema
from app.product.models import Product, ShoppingCart, PostProduct, CommentProduct

logger = logging.getLogger(__name__)

product_v1_0_bp = Blueprint('product_v1_0_bp', __name__)

product_schema = ProductSchema()
post_product_schema = PostProductSchema()
comment_product_schema = CommentProductSchema()

api = Api(product_v1_0_bp)


class ProductResource(Resource):

    def post(self):
        data = request.get_json()
        product_dict = product_schema.load(data)
        product = Product(description=product_dict['description'], price=product_dict['price'])
        product.save()
        resp = product_schema.dump(product)
        return resp, 201

    def get(self, product_id=None):
        if product_id is None:
            logger.info('Obteniendo el listado de temperaturas')
            current_app.logger.info('Obteniendo el listado de temperaturas')
            products = Product.get_all()
            result = product_schema.dump(products, many=True)
        else:
            product = Product.get_by_id(product_id)
            if product is None:
                raise ProductNotFoundException('Product not found')
            else:
                result = product_schema.dump(product)
        return result

    def put(self, product_id):
        product = Product.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundException('Product not found')
        else:
            data = request.get_json()
            product_dict = product_schema.load(data)
            product.description = product_dict['description']
            product.price = product_dict['price']
            product.commit()
            result = product_schema.dump(product)
            return result, 201

    def delete(self, product_id):
        product = Product.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundException('Product not found')
        else:
            Product.delete(product)
            return jsonify({'message': f'product with id {product_id} delete'})


class PostProductResource(Resource):

    def get(self, product_id):
        post_products = PostProduct.get_by_product(product_id)
        result = post_product_schema.dump(post_products, many=True)
        return result

    def post(self, product_id):
        data = request.get_json()
        post_product_dict = post_product_schema.load(data)
        post_product = PostProduct(title=post_product_dict['title'],
                                   product_id=product_id,
                                   content=post_product_dict['content']
                                   )
        post_product.save()
        response = post_product_schema.dump(post_product)
        return response, 201

    def put(self, product_id, post_id):
        post_product = PostProduct.get_by({'product_id': product_id, 'id': post_id})
        if post_product is None:
            raise PostProductNotFoundException('Post not found')
        else:
            data = request.get_json()
            post_product_dict = post_product_schema.load(data)
            post_product.title = post_product_dict['title']
            post_product.product_id = product_id
            post_product.content = post_product_dict['content']
            post_product.commit()
            result = post_product_schema.dump(post_product)
            return result, 201

    def delete(self, product_id, post_id):
        post_product = PostProduct.get_by({'product_id': product_id, 'id': post_id})
        if post_product is None:
            raise PostProductNotFoundException('Post not found')
        else:
            PostProduct.delete(post_product)
            return jsonify({'message': f'Post with id {post_id} was delete'})


class CommentProductResource(Resource):

    def get(self, post_id):
        comment_post_product = CommentProduct.get_by_post_id(post_id)
        result = comment_product_schema.dump(comment_post_product, many=True)
        return result

    def post(self, post_id):
        data = request.get_json()
        comment_product_dict = comment_product_schema.load(data)
        comment_product = CommentProduct(post_id=post_id, content=comment_product_dict['content'])
        comment_product.save()
        response = comment_product_schema.dump(comment_product)
        return response, 201

    def put(self, post_id, comment_id):
        parameters = {'post_id': post_id, 'id': comment_id}
        comment_product = CommentProduct.get_by(parameters)
        if comment_product is None:
            raise CommentProductNotFoundException('Comment not found')
        else:
            data = request.get_json()
            comment_product_dict = comment_product_schema.load(data)
            comment_product.post_id = post_id
            comment_product.content = comment_product_dict['content']
            comment_product.commit()
            result = comment_product_schema.dump(comment_product)
            return result, 201

    def delete(self, post_id, comment_id):
        comment_product = CommentProduct.get_by({'post_id': post_id, 'id': comment_id})
        if comment_product is None:
            raise CommentProductNotFoundException('Comment not found')
        else:
            CommentProduct.delete(comment_product)
            return jsonify({'message': f'Comment with id {comment_id} was delete'})


class UserCartResource(Resource):

    def get(self):
        results = db.session.query(User, UserCart, ShoppingCart, Product)\
            .select_from(User)\
            .join(UserCart)\
            .join(ShoppingCart)\
            .join(ShoppingCart.products).\
            order_by(desc(Product.id))\
            .all()
        logger.info(f'user_cart: {results}')

        results = [tuple(row) for row in results]

        #stmt = select(User, UserCart).join(User.carts).order_by(User.id)

        #stmt = (select(User).join(User.carts).join(UserCart.child).join(ShoppingCart.products))
        #logger.info(f'row: {stmt}')

        """stmt = select(UserCart).join_from(User, UserCart);
        for row in db.session.execute(stmt):
            logger.info(f'row: {row.UserCart.child.products}')"""

        '''user_cart = UserCart.query.filter(UserCart.user_id == 2).first()
        shopping_cart = ShoppingCart.query.filter(ShoppingCart.id == user_cart.shopping_cart_id).first()
        logger.info(f'user_cart: {user_cart.shopping_cart_id}')
        logger.info(f'shopping_cart: {shopping_cart}')'''
        return 201



api.add_resource(ProductResource,
                 '/api/v1/products',
                 '/api/v1/products/<int:product_id>'
                 )

api.add_resource(UserCartResource, '/api/v1/usercarts')

api.add_resource(PostProductResource,
                 '/api/v1/products/<int:product_id>/posts',
                 '/api/v1/products/<int:product_id>/posts/<int:post_id>'
                 )

api.add_resource(CommentProductResource,
                 '/api/v1/posts/<int:post_id>/comments',
                 '/api/v1/posts/<int:post_id>/comments/<int:comment_id>'
                 )