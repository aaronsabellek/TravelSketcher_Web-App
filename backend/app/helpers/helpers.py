import re

from flask import jsonify, current_app
from flask_login import current_user
from sqlalchemy import func, String, Text
from flask_mail import Message
from werkzeug.security import generate_password_hash

from app import db, mail
from app.models import Activity, Destination


def model_to_dict(model):
    """Returns model as dictionary"""
    return {key: getattr(model, key) for key in model.__table__.columns.keys() if not key.startswith('_')}


def models_to_list(models):
    """Returns model als list of dictionaries"""
    return [model_to_dict(model) for model in models]


def is_valid_email(email):
    """Checks if email has valid format"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.match(regex, email)


def validate_password(password):
    """Checks if password fits requirements"""

    if len(password) < 8:
        return jsonify({'error': 'Passwort has to have at least 8 characters!'}), 400
    if not any(i.isdigit() for i in password):
        return jsonify({'error': 'Passwort has to have at least one digit!'}), 400
    if not any(i.isalpha() for i in password):
        return jsonify({'error': 'Passwort has to have at least one letter!'}), 400
    if not any(not i.isalnum() for i in password):
        return jsonify({'error': 'Passwort has to have at least one special character!'}), 400

    return None


def generate_token(email, salt):
    """Generates verification token"""
    serializer = current_app.config['SERIALIZER']
    return serializer.dumps(email, salt=salt)


def confirm_token(token, salt, expiration=3600):
    """Confirms verification token"""
    try:
        serializer = current_app.config['SERIALIZER']
        email = serializer.loads(token, salt=salt, max_age=expiration)
        return email
    except:
        return None


def send_verification_email(user, salt):
    """Sends verification email to user"""

    token = generate_token(user.email, salt=salt)
    verify_url = f'/verify_email/{token}'
    subject = 'Please confirm your E-Mail'
    body = f'Click the following link to confirm your E-Mail: {verify_url}'

    send_email(user.email, subject, body)


def send_email(to_email, subject, body):
    """Sends email to user"""

    with current_app.app_context():
        sender_email = current_app.config['MAIL_DEFAULT_SENDER']
    msg = Message(subject, recipients=[to_email], body=body, sender=sender_email)
    mail.send(msg)


def update_password(user, new_password_1, new_password_2):
    """Updates password of user in database"""

    # Check for password in two fields
    if not new_password_1 or not new_password_2:
        return jsonify({'error': 'Password missing!'}), 400

    # Check if passwords match
    if new_password_1 != new_password_2:
        return jsonify({'error': 'Passwords do not match!'}), 400

    # Check if password matches the requirements
    password_validation = validate_password(new_password_1)
    if password_validation:
        return password_validation

    # Hash password
    hashed_password = generate_password_hash(new_password_1, method='pbkdf2:sha256')

    # Update hashed password in db
    user.password = hashed_password
    db.session.commit()

    return jsonify({'message': 'Password updated successfully!'}), 200


def create_search_query(model, search_query, exclude_fields):
    """
    Erstellt eine SQLAlchemy-Abfrage für eine unscharfe Suche in einem bestimmten Modell.
    Die Felder `id` und `position` sowie andere angegebene Felder werden ausgeschlossen.
    """
    # Dynamische Erstellung der Filterbedingung: Felder durchsuchen, die nicht ausgeschlossen sind
    filters = []
    for column in model.__table__.columns:
        if column.name not in exclude_fields and isinstance(column.type, (String, Text)):
            filters.append(func.lower(getattr(model, column.name)).contains(func.lower(search_query)))

    # Kombiniere alle Filter mit `or`-Verknüpfung, damit ein Treffer in einem der Felder ausreicht
    query = db.session.query(model)
    query = query.filter(
        db.or_(*filters)  # Übergebe alle Filterbedingungen als OR-Bedingung
    )

    return query


def search_resources(model, search_query):
    """Searches through strings of a specific model from user"""

    # Filter fields that will be searched
    exclude_fields = ['id', 'position', 'user_id', 'destination_id']
    filters = []

    for column in model.__table__.columns:
        if column.name not in exclude_fields and isinstance(column.type, (String, Text)):
            filters.append(func.lower(getattr(model, column.name)).contains(func.lower(search_query)))

    # Start query for model
    query = db.session.query(model)

    # Search only through entries of user
    if hasattr(model, 'user_id'):
        query = query.filter(model.user_id == current_user.id)
    elif hasattr(model, 'destination_id'):
        query = query.join(Destination).filter(Destination.user_id == current_user.id)

    # Combine filters with or-operator
    query = query.filter(db.or_(*filters))

    # Get and return results as list of dicts
    results = query.all()
    return [model_to_dict(resource) for resource in results]

