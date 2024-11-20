from models import Product, Category


def add_product_invoke(form, db, current_user):
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
    name = form.name.data
    description = form.description.data
    price = form.price.data
    amount = form.amount.data
    location = form.location.data

    # Find and assign the new category
    category = db.session.execute(
        db.select(Category).where(Category.name == form.category.data)
    ).scalar()

    image = form.image.data
    image_0 = image.read()  # Read the image file
    image_mimetype = image.mimetype  # Save the image's MIME type

    product = Product(name=name, description=description, price=price, amount=amount, status=0, location=location, category=category, image=image_0, image_mimetype=image_mimetype)

    db.session.add(product)

    # Commit changes to the database
    db.session.commit()

