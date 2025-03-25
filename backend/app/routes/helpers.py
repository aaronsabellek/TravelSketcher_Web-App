import re

from flask import jsonify, current_app
from sqlalchemy import func, String, Text
from flask_login import logout_user
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

from app import db, mail
from app.models import User, Destination, Activity


# Change Model to dict
def model_to_dict(model):
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}

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
def generate_verification_token(email):
    serializer = current_app.config['SERIALIZER']
    return serializer.dumps(email, salt='email-confirmation')

# Confirm verification token
def confirm_verification_token(token, expiration=3600):
    try:
        serializer = current_app.config['SERIALIZER']
        email = serializer.loads(token, salt='email-confirmation', max_age=expiration)
        return email
    except:
        return None

# Send email for verification
def send_verification_email(user):
    token = generate_verification_token(user.email)
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

# Create entry (User, Destination or Activity)
def create_entry(model, data, user_id=None, destination_id=None):
    # Erlaubte Felder aus dem Model holen und nur gültige Felder aus `data` übernehmen
    allowed_fields = {column.name for column in model.__table__.columns}
    data = {key: value for key, value in data.items() if key in allowed_fields}

    if not data.get('title') or data['title'] == '':
        return jsonify({'error': 'Title is required'}), 400

    # Setze die Position basierend auf existierenden Einträgen
    position_query = db.session.query(db.func.max(model.position))
    if model == Destination:
        position_query = position_query.filter_by(user_id=user_id)
    elif model == Activity:
        position_query = position_query.filter_by(destination_id=destination_id)

    #Neue Position setzen
    highest_position = position_query.scalar()
    new_position = (highest_position + 1) if highest_position is not None else 1
    data['position'] = new_position

    # Benutzer- oder Destination-ID setzen
    if user_id:
        data['user_id'] = user_id
    if destination_id:
        data['destination_id'] = destination_id

    # Initialisiere das neue Objekt mit den übergebenen Daten
    new_entry = model(**data)

    # Speichern in der Datenbank
    db.session.add(new_entry)
    db.session.commit()

    # JSON-Antwort mit den erstellten Daten zurückgeben
    return jsonify({'message': f'{model.__name__} added successfully!', model.__name__.lower(): model_to_dict(new_entry)}), 201

def get_entry(model, entry_id):
    """Hilfsfunktion, um die Daten eines Eintrags zu erhalten und zurückzugeben"""

    entry = model.query.filter_by(id=entry_id).first()
    if not entry:
        return None, 404

    # Daten extrahieren
    entry_data = {
        key: getattr(entry, key) for key in model.__table__.columns.keys() if not key.startswith('_')
    }

    return entry_data, 200

def edit_entry(model, entry_id, data, allowed_fields):
    """ Bearbeitet einen bestehenden Datenbankeintrag """
    query = model.query.filter_by(id=entry_id)
    entry = query.first()

    # Check for given entry
    if not entry:
        return jsonify({'error': f'{model.__name__} nicht gefunden oder keine Berechtigung'}), 403

    # Edit allowed fields only
    for key, value in data.items():
        if key in allowed_fields:
            setattr(entry, key, value)

    # Commit changings in db
    db.session.commit()

    # Return edited entry as dict
    return jsonify({'message': f'Updated {model.__name__} successfully!', model.__name__.lower(): model_to_dict(entry)})

def reorder_items(model, filter_by, new_order, item_name):
    """Allgemeine Funktion zur Neuanordnung von Objekten in einer bestimmten Reihenfolge."""
    if not new_order:
        return jsonify({"error": f"Die Liste {item_name} fehlt"}), 400

    # Hole alle Objekte basierend auf dem Filter
    items = model.query.filter_by(**filter_by).all()

    # Erstelle ein Dictionary für schnellen Zugriff
    item_dict = {item.id: item for item in items}

    # Überprüfe, ob alle angegebenen IDs existieren
    if set(map(int, new_order)) != set(item_dict.keys()):
        return jsonify({"error": f"Ungültige oder fehlende {item_name}-IDs"}), 400

    # Aktualisiere die Positionen
    for new_position, item_id in enumerate(new_order, start=1):
        item = item_dict[int(item_id)]
        item.position = new_position

    db.session.commit()
    return jsonify({"message": f"{item_name.capitalize()} erfolgreich umsortiert!"}), 200

def delete_item(model, item_id):
    """Allgemeine Funktion zum Löschen von Entitäten (Destinations oder Activities)"""
    item = model.query.get(item_id)

    db.session.delete(item)
    db.session.commit()

    if model == User:
        logout_user()

    return jsonify({'message': f'{model.__name__} deleted successfully'}), 200

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

