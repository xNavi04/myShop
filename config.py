from flask import Flask
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from models import db
import os
import stripe
from flask_login import LoginManager

stripe.api_key = "sk_test_51Q6BRl2N9mbjCqj3FO904WVDvLHxI167gvo593db8Av2FK19yiKNSAYm4JiOzosWhbTngLPFhEpa2M8301UsuPKR00JEXdy5hA"#os.environ.get("STRIPE_API_KEY")
endpoint_secret = "whsec_98a1720fbee9038c2393b8e5a42b861476f232f6f1eb1a31f1a5b1a100449f3d"#os.environ.get("ENDPOINT_SECRET")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "some_default_secret_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///databse.db")
    db.init_app(app)
    CKEditor(app)
    Bootstrap5(app)
    login_manager = LoginManager(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()


    return app, login_manager, db
