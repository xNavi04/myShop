from flask import render_template, request, redirect, url_for, abort, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from forms import FormProduct, InputCategory, DeleteCategoryForm, FormProductForEdit
from models import User, Product, Category, BasketProduct, Order
from base64 import b64encode
import stripe
from activity.products import get_products
from activity.product import get_product, check_if_is_product
from activity.basket import get_products_in_basket
from activity.addProduct import add_product_invoke
from activity.register import register_user
from activity.login import login_in
from activity.payment import process_checkout_or_generate_alerts
from activity.webhook import invoke_webhook
from activity.editProduct import invoke_edit_product
from activity.deleteCategory import invoke_delete_category
from activity.deleteProduct import invoke_delete_product
from activity.success import delete_all_basket_products
from decorators import get_data, manage_product, see_ware_house

def init_routes(app, login_manager, db):
    @login_manager.user_loader
    def load_user(user_id):
        return db.get_or_404(User, user_id)
    @app.route("/")
    @get_data
    def index_page(**kwargs):
        content = {
            "logged_in": current_user.is_authenticated,
            "amount": kwargs["amount"]
        }
        template = "home.html"
        return render_template(template, **content)
    @app.route("/products")
    @get_data
    def products_page(**kwargs):
        products, value, category_id, categories = get_products(db, request)
        content = {
            "logged_in": current_user.is_authenticated,
            "products": products,
            "b64encode": b64encode,
            "amount": kwargs["amount"],
            "categories": categories,
            "category_value": category_id,
            "valuee": value

        }
        template = "products.html"
        return render_template(template, **content)
    @app.route("/oneProduct/<int:num>", methods=["POST", "GET"])
    @get_data
    def one_product(num, **kwargs):
        product = db.get_or_404(Product, num)
        if request.method == "POST":
            get_product(db, num, current_user, session, request, redirect)
            return redirect(request.referrer)
        content = {
            "logged_in": current_user.is_authenticated,
            "b64encode": b64encode,
            "product": product,
            "amount": kwargs["amount"],
            "is_product": check_if_is_product(product, session, db, current_user)
            }
        template = "oneProduct.html"
        return render_template(template, **content)
    @app.route("/basket")
    @get_data
    def basket_page(**kwargs):
        products = get_products_in_basket(db, current_user, session)
        if not products:
            template = "emptyBasket.html"
        else:
            template = "basket.html"
        content = {
            "logged_in": current_user.is_authenticated,
            "basket_products": products,
            "b64encode": b64encode,
            "amount": kwargs["amount"]
        }
        return render_template(template, **content)
    @app.route("/delete/<int:num>")
    def delete_basket(num):
        product = db.get_or_404(BasketProduct, num)
        db.session.delete(product)
        db.session.commit()
        return redirect(request.referrer)
    @app.route("/addProduct", methods=["POST", "GET"])
    @login_required
    @manage_product
    @get_data
    def add_product(**kwargs):
        form = FormProduct()
        categories = db.session.execute(db.select(Category)).scalars().all()
        form.category.choices = [(category.name, category.name) for category in categories]
        if form.validate_on_submit():
            add_product_invoke(form, db, current_user)
            return redirect(url_for("products_page"))
        content = {
            "logged_in": current_user.is_authenticated,
            "form": form,
            "amount": kwargs["amount"]
        }
        template = "addProduct.html"
        return render_template(template, **content)
    @app.route("/addCategory", methods=["GET", "POST"])
    @login_required
    @manage_product
    @get_data
    def add_category(**kwargs):
        form = InputCategory()
        if form.validate_on_submit():
            name = form.name.data
            new_category = Category(name=name)
            db.session.add(new_category)
            db.session.commit()
            return redirect(url_for("products_page"))
        content = {
            "form": form,
            "amount": kwargs["amount"],
            "logged_in": current_user.is_authenticated
        }
        template = "addProduct.html"
        return render_template(template, **content)
    @app.route("/register", methods=["POST", "GET"])
    @get_data
    def register(**kwargs):
        alerts = []
        if request.method == "POST":
            x, y = register_user(request, db, alerts, login_user, generate_password_hash)
            if x == 1:
                alerts = y
            else:
                return redirect(url_for("products_page"))
        content = {
            "alerts": alerts,
            "logged_in": current_user.is_authenticated,
            "amount": kwargs["amount"]
        }
        template = "register.html"
        return render_template(template, **content)
    @app.route("/login", methods=["POST", "GET"])
    @get_data
    def login(**kwargs):
        alert = ""
        if request.method == "POST":
            x, y = login_in(request, login_user, check_password_hash, db)
            if x == 1:
              alert = y
            else:
                return redirect(url_for("products_page"))
        content = {
            "logged_in": current_user.is_authenticated,
            "alert": alert,
            "amount": kwargs["amount"]
        }
        template = "login.html"
        return render_template(template, **content)
    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for('products_page'))
    @app.route("/addOne/<int:num>")
    def add_one(num):
        basket_product = db.get_or_404(BasketProduct, num)
        if basket_product.amount + 1 <= basket_product.product.amount:
            basket_product.amount = basket_product.amount + 1
            db.session.commit()
        return redirect(request.referrer)
    @app.route("/deleteOne/<int:num>")
    def delete_one(num):
        basket_product = db.get_or_404(BasketProduct, num)
        basket_product.amount = basket_product.amount - 1
        if basket_product.amount == 0:
            db.session.delete(basket_product)
        db.session.commit()
        return redirect(request.referrer)
    @app.route("/deleteBasketProduct/<int:num>")
    def delete_basket_product(num):
        basket_product = db.get_or_404(BasketProduct, num)
        db.session.delete(basket_product)
        db.session.commit()
        return redirect(request.referrer)
    @app.route("/pay")
    @get_data
    def pay(**kwargs):
        x, y = process_checkout_or_generate_alerts(current_user, db, session, stripe)
        if x == 0:
            checkout_session = y
            return redirect(checkout_session['url'], code=303)
        elif x == -1:
            return abort(404)
        elif x == -2:
            return y
        else:
            alerts = y
            template = "lackProduct.html"
            return render_template(template, logged_in=current_user.is_authenticated, alerts=alerts, amount=kwargs["amount"])
    @app.route('/webhook', methods=['POST'])
    def webhook():
        endpoint_secret = "whsec_98a1720fbee9038c2393b8e5a42b861476f232f6f1eb1a31f1a5b1a100449f3d"
        invoke_webhook(request, stripe, endpoint_secret, db)
        return jsonify(success=True)
    @app.route("/warehouse")
    @login_required
    @see_ware_house
    @get_data
    def store(**kwargs):
        products = db.session.execute(db.select(Product)).scalars().all()
        content = {
            "products": products,
            "amount": kwargs["amount"],
            "logged_in": current_user.is_authenticated
        }
        template = "store.html"
        return render_template(template, **content)
    @app.route("/orders")
    @login_required
    @see_ware_house
    @get_data
    def orders_page(**kwargs):
        orders = db.session.execute(db.select(Order).where(Order.status == "to_implement")).scalars().all()
        content = {
            "orders": orders,
            "amount": kwargs["amount"],
            "logged_in": current_user.is_authenticated
        }
        template = "orders.html"
        return render_template(template, **content)
    @app.route("/completeOrders")
    @login_required
    @see_ware_house
    @get_data
    def complete_orders_page(**kwargs):
        orders = db.session.execute(db.select(Order).where(Order.status == "complete")).scalars().all()
        content = {
            "orders": orders,
            "amount": kwargs["amount"],
            "logged_in": current_user.is_authenticated
        }
        template = "completeOrders.html"
        return render_template(template, **content)
    @app.route("/editProduct/<int:num>", methods=["POST", "GET"])
    @login_required
    @manage_product
    @get_data
    def edit_item(num, **kwargs):
        product = db.get_or_404(Product, num)
        categories = db.session.execute(db.select(Category)).scalars().all()
        form = FormProductForEdit(name=product.name, description=product.description, price=product.price, amount=product.amount, location=product.location, category=product.category)
        form.category.choices = [(category.name, category.name) for category in categories]
        if form.validate_on_submit():
            invoke_edit_product(db, product.id, form)
        content = {
            "form": form,
            "logged_in": current_user.is_authenticated,
            "amount": kwargs["amount"]
        }
        template = "addProduct.html"
        return render_template(template, **content)
    @app.route("/deleteCategory", methods=["POST", "GET"])
    @login_required
    @manage_product
    @get_data
    def delete_category(**kwargs):
        alerts = []
        form = DeleteCategoryForm()
        categories = db.session.execute(db.select(Category)).scalars().all()
        form.name.choices = [(category.name, category.name) for category in categories]
        if form.validate_on_submit():
            x, alerts = invoke_delete_category(db, form)
            if x == 0:
                return redirect(request.referrer)
        content = {
            "form": form,
            "logged_in": current_user.is_authenticated,
            "amount": kwargs["amount"],
            "alerts": alerts
        }
        template = "addProduct.html"
        return render_template(template, **content)
    @app.route("/deleteItem/<int:num>")
    @login_required
    @manage_product
    def delete_item(num):
        invoke_delete_product(db, num)
        return redirect(request.referrer)
    @app.route("/implementOrder/<int:num>")
    @login_required
    @manage_product
    def implement_order(num):
        order = db.get_or_404(Order, num)
        order.status = "complete"
        db.session.commit()
        return redirect(request.referrer)
    @app.route("/success")
    @get_data
    def success_page(**kwargs):
        x = delete_all_basket_products(db, session, current_user)
        if x == 0:
            return abort(404)
        content = {
            "logged_in": current_user.is_authenticated,
            "amount": kwargs["amount"]
        }
        template = "success.html"
        return render_template(template, **content)
    @app.route("/denied")
    @get_data
    def deny_page(**kwargs):
        content = {
            "logged_in": current_user.is_authenticated,
            "amount": kwargs["amount"]
        }
        template = "denied.html"
        return render_template(template, **content)