import datetime

import logging
from flask import current_app
from app.tests import BaseTestClass
from app.product.models import Product
from app.product.models import PostProduct
from app.product.models import CommentProduct
from app.product.models import ShoppingCart
from app.auth.models import User, UserCart
from app import db

logger = logging.getLogger(__name__)


class ProductTestModel(BaseTestClass):

    def test_create_product_and_attach_post(self):
        with self.app.app_context():
            product = Product(description="Telefono android", price="14.5")
            product.save()

            post = PostProduct(title="Primer post", title_slug="primer-slug",
                               content="Post de prueba para producto",
                               product_id=product.id)
            post.save()

            comment = CommentProduct(content="Primer comentario para el post", post_id=post.id)
            comment.save()

            self.assertEqual("Telefono android", product.description)
            self.assertEqual(1, len(product.posts))
            self.assertEqual(1, len(post.comments))
            self.assertEqual("Telefono android", post.product_parent.description)
            self.assertEqual("Primer post", comment.post_parent.title)

    def test_save_products_in_cart(self):
        with self.app.app_context():
            product1 = Product(description="Sabanas largas", price="10")
            product1.save()

            product2 = Product(description="Colchon", price="50")
            product2.save()

            cart = ShoppingCart()
            cart.products.append(product1)
            cart.products.append(product2)

            self.assertEqual(2, len(cart.products))

            cart.save()

    def test_cart_to_user(self):
        with self.app.app_context():
            user_admin = User.get_by_email('admin@xyz.com')

            cart = ShoppingCart()

            count_products = 10

            while count_products > 0:
                description = f'Sabanas largas {count_products}'
                price = (100 + count_products)
                logger.info(f'description {description} price {price}')
                product = Product(description=description, price=price)
                cart.products.append(product)
                count_products -= 1

            cart.save()

            user_cart = UserCart(user_id=user_admin.id,
                                 shopping_cart_id=cart.id,
                                 status="created",
                                 payment_date=datetime.datetime.utcnow())

            user_admin.carts.append(user_cart)

            self.assertEqual(10, len(cart.products))
            self.assertEqual(10, len(user_admin.carts[0].child.products))

    def test_queries(self):
        with self.app.app_context():
            users = db.session.query(User).join(UserCart).filter(UserCart.user_id == User.id).all()
            logger.info(f'users {users}')
            for user in users:
                logger.info(f'users {user}')

            self.assertTrue(True)
