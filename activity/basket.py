from models import Cookie, BasketProduct


def get_or_create_session_cookie(db, session):
    """
    Retrieves or creates a session-based cookie for an anonymous user.

    Parameters:
    db: The database session object for committing changes.
    session: The session object used to store the cookie ID.

    Returns:
    The cookie ID for the session.
    """
    # Check if 'user_id' exists in the session and if the cookie exists in the database
    if "user_id" not in session or not db.session.execute(
            db.select(Cookie).where(Cookie.id == session["user_id"])).scalar():
        # If not, create a new cookie for the session
        new_cookie = Cookie()
        db.session.add(new_cookie)
        db.session.commit()  # Commit to save the new cookie to the database
        session["user_id"] = new_cookie.id  # Save the new cookie ID in the session
    return session["user_id"]


def get_basket_products_by_cookie(db, cookie_id):
    """
    Fetches basket products associated with a session-based cookie.

    Parameters:
    db: The database session object used for querying.
    cookie_id: The ID of the cookie to retrieve basket products for.

    Returns:
    A list of BasketProduct objects associated with the given cookie ID.
    """
    # Query for products in the basket based on the cookie ID
    return db.session.execute(
        db.select(BasketProduct).where(BasketProduct.cookie_id == cookie_id)
    ).scalars().all()


def get_basket_products_by_user(db, user_id):
    """
    Fetches basket products for an authenticated user.

    Parameters:
    db: The database session object used for querying.
    user_id: The ID of the authenticated user to retrieve basket products for.

    Returns:
    A list of BasketProduct objects associated with the given user ID.
    """
    # Query for products in the basket based on the user ID
    return db.session.execute(
        db.select(BasketProduct).where(BasketProduct.user_id == user_id)
    ).scalars().all()


def get_products_in_basket(db, current_user, session):
    """
    Retrieves all products in the user's shopping basket. Supports both authenticated users and session-based baskets.

    Parameters:
    db: The database session object for querying.
    current_user: The currently authenticated user (if logged in).
    session: The session object for managing non-authenticated users (via cookies).

    Returns:
    A list of products found in the basket, either for the logged-in user or the session-based user.
    """
    if not current_user.is_authenticated:
        # Handle session-based basket for anonymous users
        cookie_id = get_or_create_session_cookie(db, session)  # Retrieve or create session cookie
        products = get_basket_products_by_cookie(db, cookie_id)  # Get products for session-based user
    else:
        # Handle basket for authenticated users
        products = get_basket_products_by_user(db, current_user.id)  # Get products for logged-in user

    return products
