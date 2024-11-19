from models import BasketProduct


def remove_unavailable_products(db, basket_products):
    """
    Filters out basket products that are no longer available (amount <= 0)
    and removes them from the database.

    Parameters:
    db: The database session object for committing changes.
    basket_products: A list of BasketProduct objects to filter.

    Returns:
    A filtered list of basket products with available stock.
    """
    filtered_basket_products = basket_products[:]
    for basket_product in basket_products:
        if basket_product.product.amount <= 0:
            db.session.delete(basket_product)
            filtered_basket_products.remove(basket_product)
    db.session.commit()
    return filtered_basket_products


def get_basket_products(current_user, db, session):
    """
    Retrieves the basket products for the current user or session.

    Parameters:
    current_user: The currently logged-in user.
    db: The database session object for querying.
    session: The session object to store data for non-authenticated users.

    Returns:
    A list of BasketProduct objects or an empty list if no products are found.
    """
    if current_user.is_authenticated:
        basket_products = db.session.execute(
            db.select(BasketProduct).where(BasketProduct.user_id == current_user.id)
        ).scalars().all()
    else:
        if "user_id" not in session:
            return []
        basket_products = db.session.execute(
            db.select(BasketProduct).where(BasketProduct.cookie_id == session["user_id"])
        ).scalars().all()

    return basket_products or []


def convert_basket_products_to_json(basket_products):
    """
    Converts basket products to a JSON format suitable for Stripe checkout.

    Parameters:
    basket_products: A list of BasketProduct objects to convert.

    Returns:
    A list of dictionaries in the format required by Stripe's API.
    """
    basket_items = []
    for basket_product in basket_products:
        item = {
            "price_data": {
                "currency": "pln",
                "unit_amount": basket_product.product.price * 100,
                "product_data": {
                    "name": basket_product.product.name
                },
            },
            "quantity": basket_product.amount
        }
        basket_items.append(item)
    return basket_items


def generate_alerts_for_insufficient_stock(basket_products):
    """
    Generates alerts for products that do not have sufficient stock to fulfill the order.

    Parameters:
    basket_products: A list of BasketProduct objects to check.

    Returns:
    A list of alert messages, if any products are understocked.
    """
    alerts = []
    for basket_product in basket_products:
        if basket_product.product.amount < basket_product.amount:
            alerts.append(f"Brak produktu: {basket_product.product.name} na stanie w ilości {basket_product.amount}!")
    return alerts


def process_checkout_or_generate_alerts(current_user, db, session, stripe):
    """
    Handles checkout session creation or generates alerts for insufficient stock.

    Parameters:
    current_user: The currently logged-in user.
    db: The database session object for querying and committing changes.
    session: The session object for non-authenticated users.
    abort: Function to abort the request with a specific HTTP error.
    stripe: The Stripe object for handling payment sessions.

    Returns:
    - (1, alerts): If there are stock alerts that need user attention.
    - (0, checkout_session): If a successful Stripe checkout session was created.
    """
    basket_products = get_basket_products(current_user, db, session)

    if not basket_products:
        return -1, [] # No basket products found, return -1

    # Filter out unavailable products
    basket_products = remove_unavailable_products(db, basket_products)

    try:
        # Convert basket products to Stripe's JSON format for checkout
        converted_basket_products_to_json = convert_basket_products_to_json(basket_products)

        # Prepare metadata for Stripe
        metadata = {str(basket_product.product_id): basket_product.amount for basket_product in basket_products}

        # Create a Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            metadata=metadata,
            shipping_address_collection={"allowed_countries": ["PL"]},
            line_items=converted_basket_products_to_json,
            mode='payment',
            success_url='http://127.0.0.1:4242/success',
            cancel_url='http://127.0.0.1:4242/denied',
            automatic_tax={'enabled': True},
            locale='pl'
        )
    except stripe.error.StripeError as e:
        print("test")
        return -2, str(e)  # Handle Stripe errors

    # Generate alerts for any insufficient stock
    alerts = generate_alerts_for_insufficient_stock(basket_products)

    if alerts:
        return 1, alerts  # Return stock alerts
    else:
        return 0, checkout_session  # Return a successful checkout session
