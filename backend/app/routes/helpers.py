import re

from flask import jsonify, current_app
from sqlalchemy import func, String, Text
from flask_login import logout_user
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from werkzeug.security import generate_password_hash

from app import db, mail
from app.models import User, Destination, Activity


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

# Check existence and persmission of entry
def check_existence_and_permission(model, entry_id, user_id):

    # Check if entry exists
    entry = model.query.filter_by(id=entry_id).first()
    if not entry:
            return {'error': f'{model.__name__} not found'}, 404

    # Check permission of user
    entry = model.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return {'error': f'{model.__name__} not permitted'}, 403

    return entry

# Create entry
def create_entry(model, data, user_id=None, destination_id=None):

    # Get valid data as dict
    data = {key: value for key, value in data.items() if key in model.__table__.columns}

    # Check if required title exists
    if not data.get('title') or data['title'] == '':
        return jsonify({'error': 'Title is required'}), 400

    # Set query
    position_query = db.session.query(db.func.max(model.position))
    if model == Destination:
        position_query = position_query.filter_by(user_id=user_id)
    elif model == Activity:
        position_query = position_query.filter_by(destination_id=destination_id)

    # Set position
    highest_position = position_query.scalar()
    new_position = (highest_position + 1) if highest_position is not None else 1
    data['position'] = new_position

    # Set ID of required relationship
    if user_id:
        data['user_id'] = user_id
    if destination_id:
        data['destination_id'] = destination_id

    # Init new entry
    new_entry = model(**data)

    # Safe new entry in db
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': f'{model.__name__} added successfully!', model.__name__.lower(): model_to_dict(new_entry)}), 201

# Get entry by ID
def get_entry(model, entry_id, user_id):

    # Get entry and return error if one is thrown
    entry = check_existence_and_permission(model, entry_id, user_id)
    if isinstance(entry, tuple):
        return entry

    return model_to_dict(entry), 200

# Edit entry in db
def edit_entry(model, entry_id, data, allowed_fields=None, user_id=None):

    # Set allowed fields to standard value
    if allowed_fields is None:
        allowed_fields = [key for key in data.keys() if not key.startswith('_')]

    # Get entry
    entry = model.query.filter_by(id=entry_id).first()
    if not entry:
        return jsonify({'error': f'{model} not found'}), 404

    # Edit allowed fields only
    for key, value in data.items():
        if key in allowed_fields:
            setattr(entry, key, value)

    # Commit changings in db
    db.session.commit()

    return jsonify({'message': f'Updated {model.__name__} successfully!', model.__name__.lower(): model_to_dict(entry)}), 200

# Reorder items
def reorder_items(model, filter_by, new_order, item_name):

    # Check if there is new order from data
    if not new_order:
        return jsonify({'error': f'The list of {item_name} is missing'}), 400

    # Get all items needed as dict
    items = model.query.filter_by(**filter_by).all()
    item_dict = {item.id: item for item in items}

    # Check if all the IDs exist
    if set(map(int, new_order)) != set(item_dict.keys()):
        return jsonify({'error': f'Invalid or missing IDs of {item_name}'}), 400

    # Reorder items
    for new_position, item_id in enumerate(new_order, start=1):
        item = item_dict[int(item_id)]
        item.position = new_position

    # Update db
    db.session.commit()

    return jsonify({'message': f'Reordered {item_name.capitalize()} successfully!'}), 200

# Delete item
def delete_item(model, item_id):

    # Get item by id
    item = model.query.filter_by(id=item_id).first()

    # Delete item in db
    db.session.delete(item)
    db.session.commit()

    # Logout if item is user
    if model == User:
        logout_user()

    return jsonify({'message': f'{model.__name__} deleted successfully!'}), 200

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

