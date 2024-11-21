from flask import Flask
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from models import db
import os
import stripe
from flask_login import LoginManager

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "sadjfh98w7eh32ijfnijof2h3iofh23ijofhi3h2")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///databse.db")
    db.init_app(app)
    CKEditor(app)
    Bootstrap5(app)
    login_manager = LoginManager(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()


    return app, login_manager, db, endpoint_secret
