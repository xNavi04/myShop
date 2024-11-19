from models import Product, Order, BasketProduct


def create_order(event, db):
    """
    Creates an order in the database based on the event data from Stripe.

    Parameters:
    event: The Stripe webhook event containing order details.
    db: The database session object used for querying and committing.

    Returns:
    None
    """
    if event['type'] == 'checkout.session.completed':
        order_details = extract_order_details(event)
        product_metadata = event['data']['object']['metadata']

        body = generate_order_body(product_metadata, db)
        amount_total = int(event['data']['object']['amount_total']) * 0.01

        new_order = Order(
            city=order_details['city'],
            country=order_details['country'],
            line_1=order_details['line1'],
            line_2=order_details['line2'],
            postal_code=order_details['postal_code'],
            amount_total=amount_total,
            body=body,
            status="to_implement"
        )

        db.session.add(new_order)
        db.session.commit()
    else:
        print(f'Unhandled event type {event["type"]}')


def extract_order_details(event):
    """
    Extracts shipping details from the event data.

    Parameters:
    event: The Stripe webhook event containing shipping details.

    Returns:
    dict: A dictionary containing the extracted shipping details.
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
    Generates the order body text and updates the product quantities.

    Parameters:
    product_metadata: The metadata containing product IDs and quantities.
    db: The database session object used for querying.

    Returns:
    str: A formatted string representing the order body.
    """
    body = ""

    for product_id in product_metadata:
        product = db.get_or_404(Product, product_id)
        quantity = int(product_metadata[product_id])

        body += f"id={product.id} name={product.name} amount={quantity}   //   "
        product.amount -= quantity  # Update product amount
        delete_products_from_basket(product, quantity, db)

    return body

def invoke_webhook(request, stripe, endpoint_secret, db):
    """
    Handles incoming webhook requests from Stripe and verifies the signature.

    Parameters:
    request: The incoming request containing the webhook data.
    stripe: The Stripe library instance.
    endpoint_secret: The secret for verifying webhook signatures.
    db: The database session object used for querying and committing.

    Returns:
    None
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
    basket_products = db.session.execute(db.select(BasketProduct)).scalars().all()

    for basket_product in basket_products:
        if basket_product.product_id == product.id:
            if basket_product.amount <= quantity:
                db.session.delete(basket_product)
            db.session.commit()



