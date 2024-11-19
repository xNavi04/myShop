from models import User
import re  # For email validation

def is_valid_email(email):
    """
    Validates the format of an email address.

    Parameters:
    - email (str): The email address to validate.

    Returns:
    - bool: True if the email format is valid, otherwise False.
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_form_data_invalid(username, email, password):
    """
    Checks if any required form fields are empty.

    Parameters:
    - username (str): The entered username.
    - email (str): The entered email address.
    - password (str): The entered password.

    Returns:
    - bool: True if any field is empty, otherwise False.
    """
    return not username or not email or not password

def do_passwords_match(password, confirm_password):
    """
    Checks if the password and confirmation password match.

    Parameters:
    - password (str): The password entered by the user.
    - confirm_password (str): The password confirmation entered by the user.

    Returns:
    - bool: True if the passwords match, otherwise False.
    """
    return password == confirm_password

def user_exists(db, email, username):
    """
    Checks if a user with the specified email or username already exists in the database.

    Parameters:
    - db (SQLAlchemy): The database session object for querying.
    - email (str): The email address to check.
    - username (str): The username to check.

    Returns:
    - User or None: Returns the user if found, otherwise None.
    """
    user_by_email = db.session.execute(db.select(User).where(User.email == email)).scalar()
    user_by_username = db.session.execute(db.select(User).where(User.username == username)).scalar()
    return user_by_email or user_by_username

def create_new_user(db, username, email, password, generate_password_hash):
    """
    Creates a new user and saves it to the database.

    Parameters:
    - db (SQLAlchemy): The database session object for committing changes.
    - username (str): The username for the new user.
    - email (str): The email for the new user.
    - password (str): The plaintext password for the new user.
    - generate_password_hash (function): A function to hash the password.

    Returns:
    - User: The newly created User object.
    """
    hash_password = generate_password_hash(password, salt_length=8)
    new_user = User(username=username,
                    email=email,
                    password=hash_password,
                    permission=0)

    db.session.add(new_user)
    db.session.commit()
    return new_user

def register_user(request, db, alerts, login_user, generate_password_hash):
    """
    Manages user registration, including validation and database insertion.

    Parameters:
    - request (flask.Request): The HTTP request object containing form data.
    - db (SQLAlchemy): The database session object for querying and committing changes.
    - alerts (list): A list to hold alert messages for validation issues.
    - login_user (function): A function that logs in the newly registered user.
    - generate_password_hash (function): A function to hash the user password.

    Returns:
    - tuple: (int, list)
        - 0 and an empty list if registration is successful.
        - 1 and a list of alert messages if registration fails.
    """
    # Retrieve data from the form
    username = request.form.get("username", "")
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirmPassword", "")

    # Form data validation
    if user_exists(db, email, username):
        alerts.append("This user already exists or the username is taken!")
    elif not do_passwords_match(password, confirm_password):
        alerts.append("Passwords do not match!")
    elif is_form_data_invalid(username, email, password):
        alerts.append("Some fields are empty!")
    elif not is_valid_email(email):
        alerts.append("The email format is invalid!")
    else:
        # Create and log in the new user
        new_user = create_new_user(db, username, email, password, generate_password_hash)
        login_user(new_user)
        return 0, []
    return 1, alerts
