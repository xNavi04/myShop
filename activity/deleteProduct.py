from models import Product, BasketProduct


def find_product_by_id(db, product_id):
    """
    Finds a product by its ID, or returns a 404 error if not found.

    Parameters:
    db: The database session object used for querying.
    product_id: The ID of the product to retrieve.

    Returns:
    The Product object if found, otherwise raises a 404 error.
    """
    return db.get_or_404(Product, product_id)


def find_basket_products_by_product_id(db, product_id):
    """
    Retrieves all basket products associated with a specific product.

    Parameters:
    db: The database session object used for querying.
    product_id: The ID of the product to find associated basket products.

    Returns:
    A list of BasketProduct objects associated with the given product ID.
    """
    return db.session.execute(
        db.select(BasketProduct).where(BasketProduct.product_id == product_id)
    ).scalars().all()


def delete_basket_products(db, basket_products):
    """
    Deletes all basket products passed in the list.

    Parameters:
    db: The database session object for committing changes.
    basket_products: A list of BasketProduct objects to delete.

    Returns:
    None
    """
    for basket_product in basket_products:
        db.session.delete(basket_product)


def delete_product(db, product):
    """
    Deletes a product from the database.

    Parameters:
    db: The database session object for committing changes.
    product: The Product object to delete.

    Returns:
    None
    """
    db.session.delete(product)


def invoke_delete_product(db, num):
    """
    Deletes a product and its associated basket products from the database.

    Parameters:
    db: The database session object for querying and committing changes.
    num: The ID of the product to delete.

    Returns:
    None
    """
    # Find the product by its ID
    product = find_product_by_id(db, num)

    # Find and delete all associated basket products
    basket_products = find_basket_products_by_product_id(db, product.id)
    delete_basket_products(db, basket_products)

    # Delete the product itself
    delete_product(db, product)

    # Commit all changes to the database
    db.session.commit()
