from models import Product, Category

def update_product_with_form_data(product, form, db):
    """
    Updates a Product object with data from a form and commits changes to the database.

    Parameters:
    - product (Product): The Product object to update.
    - form (formProductForEdit): The form containing updated product data.
    - db (SQLAlchemy): The database session object for committing changes.

    Returns:
    None
    """
    # Update product fields with form data
    product.name = form.name.data
    product.description = form.description.data
    product.price = form.price.data
    product.amount = form.amount.data
    product.location = form.location.data

    # Find and assign the new category
    product.category = db.session.execute(
        db.select(Category).where(Category.name == form.category.data)
    ).scalar()

    # If a new image was uploaded, update the product's image
    if form.image.data:
        image = form.image.data
        product.image = image.read()  # Read the image file
        product.image_mimetype = image.mimetype  # Save the image's MIME type

    # Commit changes to the database
    db.session.commit()


def find_product_by_id(db, product_id):
    """
    Retrieves a Product object by its ID, raising a 404 error if not found.

    Parameters:
    - db (SQLAlchemy): The database session object used for querying.
    - product_id (int): The ID of the product to retrieve.

    Returns:
    Product: The Product object if found, otherwise raises a 404 error.
    """
    return db.get_or_404(Product, product_id)


def invoke_edit_product(db, product_id, form):
    """
    Handles the process of editing a product by updating it with data from a form.

    Parameters:
    - db (SQLAlchemy): The database session object for querying and committing changes.
    - product_id (int): The ID of the Product object to be edited.
    - form (formProductForEdit): The form containing updated data to apply to the product.

    Returns:
    None
    """
    # Find the product by its ID
    product = db.get_or_404(Product, product_id)
    # Update the product with form data
    update_product_with_form_data(product, form, db)
