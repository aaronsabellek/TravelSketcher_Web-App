from flask import jsonify

from models import db, User, Destination, Activity


def model_to_dict(model):
    """Wandelt ein SQLAlchemy-Objekt in ein Dictionary um."""
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}

def models_to_list(models):
    """Wandelt eine Liste von SQLAlchemy-Objekten in eine Liste von Dictionaries um."""
    return [model_to_dict(model) for model in models]

def check_unique_username(new_username):
    if not new_username:
        return jsonify({'error': 'Neuer Benutzername ist erforderlich'}), 400

    if User.query.filter_by(username=new_username).first():
        return jsonify({'error': 'Dieser Benutzername ist bereits vergeben'}), 400

#Funktion zum Hinzufügen eines Objekts zur Datenbank (Destination oder Activity)
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

def edit_entry(model, entry_id, user_id=None, destination_id=None, data=None):
    """ Bearbeitet einen bestehenden Datenbankeintrag """

    # Passendes Model-Objekt abrufen
    query = model.query.filter_by(id=entry_id)
    # Falls es sich um eine Destination handelt, prüfen, ob sie dem Nutzer gehört
    if model == Destination:
        query = query.filter_by(user_id=user_id)
    elif model == Activity and destination_id:
        query = query.filter_by(destination_id=destination_id)
    entry = query.first()

    # Falls kein Eintrag gefunden oder keine Berechtigung, Fehler zurückgeben
    if not entry:
        return jsonify({'error': f'{model.__name__} nicht gefunden oder keine Berechtigung'}), 403

    # Erlaubte Felder abrufen
    allowed_fields = {column.name for column in model.__table__.columns}

    # Nur erlaubte Werte aktualisieren
    print(data.items)
    for key, value in data.items():
        if key in allowed_fields:
            setattr(entry, key, value)

    # Änderungen speichern
    db.session.commit()

    return jsonify({'message': f'{model.__name__} erfolgreich aktualisiert!', model.__name__.lower(): model_to_dict(entry)})

