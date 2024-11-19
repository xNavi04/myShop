from models import Category, Product


def get_products(db, request):
    """
    Retrieves products based on optional filters for category and price.

    Parameters:
    db: The database session object.
    request: The request object containing query parameters.

    Returns:
    A tuple containing:
        - products: The filtered list of products.
        - value: The filter value corresponding to the selected price range.
        - category_id: The ID of the selected category.
        - categories: The list of all categories available.
    """
    # Retrieve all categories from the database
    categories = db.session.execute(db.select(Category)).scalars().all()

    # Get filter criteria from request arguments
    category_id = request.args.get("category")
    price = request.args.get("price")

    # Determine which filter(s) to apply
    if price and category_id:
        products, value = get_products_for_filter_price_and_category(db, price, category_id)
    elif category_id:
        products, value = get_products_for_filter_category(db, category_id)
    elif price:
        products, value = get_products_for_filter_price(db, price)
    else:
        # If no filters are applied, retrieve all products
        products = db.session.execute(db.select(Product)).scalars().all()
        value = None

    return products, value, category_id, categories


def get_products_for_filter_price_and_category(db, price, category_id):
    """
    Retrieves products filtered by both price range and category.

    Parameters:
    db: The database session object.
    price: The price range identifier.
    category_id: The ID of the category to filter by.

    Returns:
    A tuple containing:
        - products: The list of filtered products.
        - value: The filter value corresponding to the selected price range.
    """
    if price == "1":
        value = 1
        products = db.session.execute(
            db.select(Product).where(Product.category_id == category_id, Product.price < 500)
        ).scalars().all()
    elif price == "2":
        value = 2
        products = db.session.execute(
            db.select(Product).where(Product.category_id == category_id, Product.price >= 500, Product.price <= 1000)
        ).scalars().all()
    elif price == "3":
        value = 3
        products = db.session.execute(
            db.select(Product).where(Product.category_id == category_id, Product.price > 1000, Product.price <= 5000)
        ).scalars().all()
    elif price == "4":
        value = 4
        products = db.session.execute(
            db.select(Product).where(Product.category_id == category_id, Product.price > 5000)
        ).scalars().all()
    else:
        products = None
        value = None

    return products, value


def get_products_for_filter_category(db, category_id):
    """
    Retrieves products filtered by category.

    Parameters:
    db: The database session object.
    category_id: The ID of the category to filter by.

    Returns:
    A tuple containing:
        - products: The list of products in the specified category.
        - value: None (no price filter applied).
    """
    value = None
    return db.session.execute(
        db.select(Product).where(Product.category_id == category_id)
    ).scalars().all(), value


def get_products_for_filter_price(db, price):
    """
    Retrieves products filtered by price range.

    Parameters:
    db: The database session object.
    price: The price range identifier.

    Returns:
    A tuple containing:
        - products: The list of products in the specified price range.
        - value: The filter value corresponding to the selected price range.
    """
    if price == "1":
        value = 1
        products = db.session.execute(
            db.select(Product).where(Product.price < 500)
        ).scalars().all()
    elif price == "2":
        value = 2
        products = db.session.execute(
            db.select(Product).where(Product.price >= 500, Product.price <= 1000)
        ).scalars().all()
    elif price == "3":
        value = 3
        products = db.session.execute(
            db.select(Product).where(Product.price > 1000, Product.price <= 5000)
        ).scalars().all()
    elif price == "4":
        value = 4
        products = db.session.execute(
            db.select(Product).where(Product.price > 5000)
        ).scalars().all()
    else:
        products = None
        value = None

    return products, value
