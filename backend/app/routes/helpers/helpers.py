import re

from flask import jsonify, current_app
from sqlalchemy import func, String, Text
from flask_mail import Message
from werkzeug.security import generate_password_hash

from app import db, mail


# Change Model to dict
def model_to_dict(model):
    return {key: getattr(model, key) for key in model.__table__.columns.keys() if not key.startswith('_')}

# Change Model to list of dicts
def models_to_list(models):
    return [model_to_dict(model) for model in models]

# Check if email has valid format
def is_valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.match(regex, email)

# Check if password fits requirements
def validate_password(password):
    if len(password) < 8:
        return jsonify({'error': 'Passwort has to have at least 8 characters!'}), 400
    if not any(i.isdigit() for i in password):
        return jsonify({'error': 'Passwort has to have at least one digit!'}), 400
    if not any(i.isalpha() for i in password):
        return jsonify({'error': 'Passwort has to have at least one letter!'}), 400
    if not any(not i.isalnum() for i in password):
        return jsonify({'error': 'Passwort has to have at least one special character!'}), 400
    return None

# Generate verificatoin token
def generate_token(email, salt):
    serializer = current_app.config['SERIALIZER']
    return serializer.dumps(email, salt=salt)

# Confirm verification token
def confirm_token(token, salt, expiration=3600):
    try:
        serializer = current_app.config['SERIALIZER']
        email = serializer.loads(token, salt=salt, max_age=expiration)
        return email
    except:
        return None

# Send email for verification
def send_verification_email(user, salt):
    token = generate_token(user.email, salt=salt)
    verify_url = f'/verify_email/{token}'
    subject = 'Please confirm your E-Mail'
    body = f'Click the following link to confirm your E-Mail: {verify_url}'

    send_email(user.email, subject, body)

# Send email
def send_email(to_email, subject, body):
    with current_app.app_context():
        sender_email = current_app.config['MAIL_DEFAULT_SENDER']
    msg = Message(subject, recipients=[to_email], body=body, sender=sender_email)
    mail.send(msg)

# Update password
def update_password(user, new_password_1, new_password_2):

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

def search_resources(model, search_query, exclude_fields):
    """
    Führt eine Suche für das gegebene Modell aus und gibt die Ergebnisse als Liste von Dictionaries zurück.
    """
    query = create_search_query(model, search_query, exclude_fields)
    results = query.all()
    return [model_to_dict(resource) for resource in results]

