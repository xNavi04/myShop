from functools import wraps
from flask import session, abort
from flask_login import current_user
from models import BasketProduct

def get_data(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        logged_in = current_user.is_authenticated
        from app import db
        if not logged_in:
            if "user_id" not in session:
                amount = 0
            else:
                basket_products = db.session.execute(db.select(BasketProduct).where(BasketProduct.cookie_id == session["user_id"])).scalars().all()
                basket_products = [basket_products for basket_product in basket_products if basket_product.product.amount >= 1]
                amount = len(basket_products)
        else:
            basket_products = db.session.execute(db.select(BasketProduct).where(BasketProduct.user_id == current_user.id)).scalars().all()
            basket_products = [basket_products for basket_product in basket_products if basket_product.product.amount >= 1]
            amount = len(basket_products)
        kwargs['amount'] = amount
        return f(*args, **kwargs)
    return decorator_function

def admin_only(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        if current_user.id == 1:
            return f(*args, **kwargs)
        else:
            return abort(404)
    return decorator_function


def manage_product(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        if current_user.permission >= 2:
            return f(*args, **kwargs)
        else:
            return abort(404)
    return decorator_function


def see_ware_house(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        if current_user.permission >= 1:
            return f(*args, **kwargs)
        else:
            return abort(404)
    return decorator_function