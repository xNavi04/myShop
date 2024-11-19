from models import User


def login_in(request, login_user, check_password_hash, db):
    """
    Handles user login by verifying email and password credentials.

    Parameters:
    - request (flask.Request): The HTTP request object containing form data for email and password.
    - login_user (function): A function that logs in a user in the current session.
    - check_password_hash (function): A function to validate the hashed password with the input password.
    - db (SQLAlchemy): The database instance for querying user data.

    Returns:
    - tuple: (int, str or None)
        - (0, None) if the login is successful.
        - (1, alert) where `alert` is a message describing the failure reason.

    Alert Messages:
    - "Something is empty!" if either the email or password field is empty.
    - "This user does not exist!" if the email does not match any user.
    - "Wrong password" if the password is incorrect.

    Example:
    >>> status, alert = login_in(request, login_user, check_password_hash, db)
    >>> if status == 0:
    >>>     print("Login successful")
    >>> else:
    >>>     print(f"Login failed: {alert}")
    """
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    if not email or not password:
        return 1, "Something is empty!"

    user = db.session.execute(db.select(User).where(User.email == email)).scalar()

    if not user:
        return 1, "This user does not exist!"

    if check_password_hash(user.password, password):
        login_user(user)
        return 0, None
    else:
        return 1, "Wrong password"
