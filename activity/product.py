from flask import abort

from models import BasketProduct, Cookie, Product, User

def create_cookie(db, session):
    """
    Creates a new Cookie object and saves it in the database and user session.

    Parameters:
    db: The database session object.
    session: The user session.

    Returns:
    None
    """
    new_cookie = Cookie()
    db.session.add(new_cookie)
    db.session.commit()
    session["user_id"] = new_cookie.id


def add_product_to_basket_for_guest(db, product, amount, session):
    """
    Adds a product to the basket for a guest user (not authenticated).

    Parameters:
    db: The database session object.
    product: The Product object to be added.
    amount: The quantity of the product to add.
    session: The user session.

    Returns:
    None
    """
    # Ensure the guest user has an associated cookie, create one if not
    if "user_id" not in session or not (
        db.session.execute(db.select(Cookie).where(Cookie.id == session["user_id"])).scalar()):
        create_cookie(db, session)

    # Check if the product is already in the basket
    basket_product = db.session.execute(
        db.select(BasketProduct).where(BasketProduct.product_id == product.id,
                                        BasketProduct.cookie_id == session["user_id"])
    ).scalar()

    if basket_product:
        # Increment the quantity of the existing product in the basket
        basket_product.amount += int(amount)
    else:
        # Add a new product to the basket
        cookie = db.get_or_404(Cookie, session["user_id"])
        new_basket_product = BasketProduct(cookie=cookie, product=product, amount=int(amount))
        db.session.add(new_basket_product)


def add_product_to_basket_for_user(db, product, amount, current_user):
    """
    Adds a product to the basket for an authenticated user.

    Parameters:
    db: The database session object.
    product: The Product object to be added.
    amount: The quantity of the product to add.
    current_user: The authenticated user.

    Returns:
    None
    """
    # Check if the product is already in the basket
    basket_product = db.session.execute(
        db.select(BasketProduct).where(BasketProduct.product_id == product.id,
                                        BasketProduct.user_id == current_user.id)
    ).scalar()

    if basket_product:
        # Increment the quantity of the existing product in the basket
        basket_product.amount += int(amount)
    else:
        # Add a new product to the basket
        user = db.get_or_404(User, current_user.id)
        new_basket_product = BasketProduct(user=user, product=product, amount=int(amount))
        db.session.add(new_basket_product)


def get_product(db, num, current_user, session, request, redirect):
    """
    Retrieves a product, validates it, adds it to the basket, and redirects the user.

    Parameters:
    db: The database session object.
    num: The ID of the product to retrieve.
    current_user: The authenticated user.
    session: The user session.
    request: The HTTP request object.
    redirect: The redirect function.

    Returns:
    Redirects the user to the referring page.
    """
    # Fetch the product from the database
    product = db.get_or_404(Product, num)
    amount = request.form["amount"]
    if int(amount) == 0:
        return abort(404)

    # Add product to the basket for either a guest or authenticated user
    if not current_user.is_authenticated:
        # For guest users, validate and update the basket
        basket_products = db.session.execute(
            db.select(BasketProduct).where(BasketProduct.cookie_id == session["user_id"])
        ).scalars().all()
        if not basket_products:
            if int(amount) > product.amount:
                return abort(404)
        else:
            for basket_product in basket_products:
                if basket_product.product_id == product.id:
                    if basket_product.amount + int(amount) > product.amount:
                        return abort(404)
        add_product_to_basket_for_guest(db, product, amount, session)
    else:
        # For authenticated users, validate and update the basket
        if not current_user.basketProducts:
            if int(amount) > product.amount:
                return abort(404)
        else:
            for basket_product in current_user.basketProducts:
                if basket_product.product_id == product.id:
                    if basket_product.amount + int(amount) > product.amount:
                        return abort(404)
        add_product_to_basket_for_user(db, product, amount, current_user)

    # Commit changes to the database
    db.session.commit()

    return redirect(request.referrer)


def check_if_is_product(product, session, db, current_user, amount=1):
    """
    Checks if the product can be added to the basket based on stock and user status.

    Parameters:
    product: The Product object to check.
    session: The user session.
    db: The database session object.
    current_user: The authenticated user.
    amount: The quantity to be added (default is 1).

    Returns:
    0 if the product can be added, 1 if not.
    """
    if current_user.is_authenticated:
        # For authenticated users, check stock and basket
        if not current_user.basketProducts:
            if int(amount) > product.amount:
                return 1
        for basket_product in current_user.basketProducts:
            if basket_product.product_id == product.id:
                if basket_product.amount + int(amount) > product.amount:
                    return 1
    else:
        # For guest users, ensure cookie and validate stock
        if "user_id" not in session or not (
                db.session.execute(db.select(Cookie).where(Cookie.id == session["user_id"])).scalar()):
            create_cookie(db, session)

        basket_products = db.session.execute(db.select(BasketProduct).where(BasketProduct.cookie_id == session["user_id"])).scalars().all()

        if not basket_products:
            if int(amount) > product.amount:
                return 1

        for basket_product in basket_products:
            if basket_product.product_id == product.id:
                if basket_product.amount + int(amount) > product.amount:
                    return 1
    return 0
