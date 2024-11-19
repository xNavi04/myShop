from models import BasketProduct

def delete_all_basket_products(db, session, current_user):
    """
    Deletes all products from the user's shopping basket.

    Parameters:
    db: The database session object used for querying and committing changes.
    session: The session object that contains user-related information.
    current_user: The currently authenticated user.

    Returns:
    int: Returns 1 if no user ID is found in the session; otherwise, returns None.
    """
    # Check if there is a user ID in the session
    if "user_id" not in session:
        return 1  # Return 1 if no user ID is found

    # Retrieve the basket products for the user
    basket_products = get_basket_products(db, session, current_user)

    # If there are basket products, delete them
    if basket_products:
        delete_basket_products(db, basket_products)


def get_basket_products(db, session, current_user):
    """
    Retrieves the basket products for the current user.

    Parameters:
    db: The database session object used for querying.
    session: The session object that contains user-related information.
    current_user: The currently authenticated user.

    Returns:
    list: A list of BasketProduct objects belonging to the user.
    """
    if not current_user.is_authenticated:
        # Fetch basket products using the cookie ID for unauthenticated users
        return db.session.execute(
            db.select(BasketProduct).where(BasketProduct.cookie_id == session["user_id"])
        ).scalars().all()
    else:
        # Fetch basket products using the user ID for authenticated users
        return db.session.execute(
            db.select(BasketProduct).where(BasketProduct.user_id == current_user.id)
        ).scalars().all()


def delete_basket_products(db, basket_products):
    """
    Deletes the specified basket products from the database.

    Parameters:
    db: The database session object used for committing changes.
    basket_products: A list of BasketProduct objects to delete.

    Returns:
    None
    """
    # Iterate through the basket products and delete each one
    for basket_product in basket_products:
        db.session.delete(basket_product)

    # Commit the changes to the database
    db.session.commit()
