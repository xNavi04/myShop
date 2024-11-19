from models import Category


def find_category_by_name(db, category_name):
    """
    Finds a category in the database by its name.

    Parameters:
    db: The database session object used for querying.
    category_name: The name of the category to search for.

    Returns:
    The Category object if found, otherwise None.
    """
    return db.session.execute(db.select(Category).where(Category.name == category_name)).scalar()


def category_has_products(category):
    """
    Checks if the category has any associated products.

    Parameters:
    category: The Category object to check.

    Returns:
    True if the category has products, otherwise False.
    """
    return bool(category.products)  # Assuming 'category.products' is a relationship in the model


def delete_category(db, category):
    """
    Deletes the given category from the database.

    Parameters:
    db: The database session object for committing changes.
    category: The Category object to delete.

    Returns:
    None
    """
    db.session.delete(category)
    db.session.commit()


def invoke_delete_category(db, form):
    """
    Handles the deletion of a category based on form data. Ensures that no products are associated with the category before deletion.

    Parameters:
    db: The database session object for querying and committing changes.
    form: The form object containing the category data (e.g., category name).

    Returns:
    A tuple with a status code and a list of alerts.
    - Status code 1 means the deletion failed (due to associated products).
    - Status code 0 means the deletion succeeded.
    """
    alerts = []

    # Validate the form before proceeding
    category_name = form.name.data

    # Find the category in the database
    category = find_category_by_name(db, category_name)

    if not category:
        alerts.append(f"Category '{category_name}' not found.")
        return 1, alerts

    # Check if the category has associated products
    if category_has_products(category):
        alerts.append("You have to delete items with this category before deleting the category.")
        return 1, alerts

    # Delete the category if no products are associated
    delete_category(db, category)
    alerts.append(f"Category '{category_name}' deleted successfully.")
    return 0, alerts
