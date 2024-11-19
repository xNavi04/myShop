from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    permission = db.Column(db.Integer, nullable=False)
    products = db.relationship("Product", back_populates="owner")
    basketProducts = db.relationship("BasketProduct", back_populates="user")

class Cookie(db.Model):
    __tablename__ = "cookies"
    id = db.Column(db.Integer, primary_key=True)
    basket_products = db.relationship("BasketProduct", back_populates="cookie")


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    image_mimetype = db.Column(db.String, nullable=False)
    owner = db.relationship("User", back_populates="products")
    basketProducts = db.relationship("BasketProduct", back_populates="product")
    category = db.relationship("Category", back_populates="products")

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    products = db.relationship("Product", back_populates="category")

class BasketProduct(db.Model):
    __tablename__ = "basketProducts"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    cookie_id = db.Column(db.Integer, db.ForeignKey("cookies.id"))
    amount = db.Column(db.Integer, nullable=False)
    product = db.relationship("Product", back_populates="basketProducts")
    user = db.relationship("User", back_populates="basketProducts")
    cookie = db.relationship("Cookie", back_populates="basket_products")

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    line_1 = db.Column(db.String, nullable=False)
    line_2 = db.Column(db.String, nullable=True)
    postal_code = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    amount_total = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)