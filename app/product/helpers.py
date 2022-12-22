import datetime

from app.auth.models import UserCart, User
from app.product.models import ShoppingCart, Product

import logging

logger = logging.getLogger(__name__)


def make_user_cart(self):
    user_admin = User.get_by_email('admin@xyz.com')

    cart = ShoppingCart()

    count_products = 10

    while count_products > 1:
        product = Product.get_by_id(count_products)
        logger.info(f'description {product.description} price {product.price}')
        cart.products.append(product)
        count_products -= 1

    cart.save()

    user_cart = UserCart(user_id=user_admin.id,
                         shopping_cart_id=cart.id,
                         status="created",
                         payment_date=datetime.datetime.utcnow())

    user_cart.save()

    user_admin.carts.append(user_cart)
    user_admin.save()
