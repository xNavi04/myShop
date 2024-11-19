from models import Product, Order, BasketProduct


def create_order(event, db):
    """
    Creates a new order in the database using data from a Stripe webhook event.

    Parameters:
    - event (dict): Stripe webhook event containing order details.
    - db: SQLAlchemy database session used for querying and committing transactions.

    Returns:
    None
    """
    if event['type'] == 'checkout.session.completed':
        order_details = extract_order_details(event)
        product_metadata = event['data']['object']['metadata']

        body = generate_order_body(product_metadata, db)
        amount_total = int(event['data']['object']['amount_total']) * 0.01  # Convert amount from cents to currency

        new_order = Order(
            city=order_details['city'],
            country=order_details['country'],
            line_1=order_details['line1'],
            line_2=order_details['line2'],
            postal_code=order_details['postal_code'],
            amount_total=amount_total,
            body=body,
            status="to_implement"  # Initial status for the order
        )

        db.session.add(new_order)
        db.session.commit()
    else:
        print(f'Unhandled event type {event["type"]}')


def extract_order_details(event):
    """
    Extracts shipping address details from a Stripe webhook event.

    Parameters:
    - event (dict): Stripe webhook event containing shipping information.

    Returns:
    dict: Extracted shipping address details including city, country, lines, and postal code.
    """
    shipping_details = event['data']['object']['shipping_details']['address']
    if not shipping_details['line2']:
        x = ""
    else:
        x = shipping_details['line2']
    return {
        'city': shipping_details['city'],
        'country': shipping_details['country'],
        'line1': shipping_details['line1'],
        'line2': x,
        'postal_code': shipping_details['postal_code']
    }


def generate_order_body(product_metadata, db):
    """
    Creates a descriptive summary of the order and updates product quantities in the inventory.

    Parameters:
    - product_metadata (dict): Metadata containing product IDs and their ordered quantities.
    - db: SQLAlchemy database session used for querying and committing updates.

    Returns:
    str: A string summarizing the order details.
    """
    body = ""

    for product_id in product_metadata:
        product = db.get_or_404(Product, product_id)
        quantity = int(product_metadata[product_id])

        body += f"id={product.id} name={product.name} amount={quantity}   //   "
        product.amount -= quantity  # Deduct ordered quantity from inventory
        delete_products_from_basket(product, quantity, db)

    return body


def invoke_webhook(request, stripe, endpoint_secret, db):
    """
    Processes Stripe webhook requests by verifying the signature and invoking the appropriate handler.

    Parameters:
    - request: Incoming HTTP request containing the webhook payload.
    - stripe: Stripe library instance for verifying the webhook signature.
    - endpoint_secret (str): Secret key for validating webhook signatures.
    - db: SQLAlchemy database session used for further operations.

    Returns:
    None

    Raises:
    - ValueError: If the payload is invalid.
    - stripe.error.SignatureVerificationError: If the signature is invalid.
    """
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e

    create_order(event, db)


def delete_products_from_basket(product, quantity, db):
    """
    Removes or updates products in the user's basket based on the ordered quantity.

    Parameters:
    - product (Product): The product being ordered.
    - quantity (int): Quantity of the product to be removed from the basket.
    - db: SQLAlchemy database session used for querying and committing updates.

    Returns:
    None
    """
    basket_products = db.session.execute(db.select(BasketProduct)).scalars().all()

    for basket_product in basket_products:
        if basket_product.product_id == product.id:
            if basket_product.amount <= quantity:
                db.session.delete(basket_product)  # Remove item if ordered quantity is greater or equal
            db.session.commit()
