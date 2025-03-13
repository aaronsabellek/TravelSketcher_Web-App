from flask import jsonify

from models import db, Destination, Activity


#Funktion zum Hinzufügen eines Objekts zur Datenbank (Destination oder Activity)
def create_entry(model, data, user_id=None, destination_id=None):

    # Erlaubte Felder aus dem Model holen und nur gültige Felder aus `data` übernehmen
    allowed_fields = {column.name for column in model.__table__.columns}
    data = {key: value for key, value in data.items() if key in allowed_fields}

    # Setze die Position basierend auf existierenden Einträgen
    position_query = db.session.query(db.func.max(model.position))
    if model == Destination:
        position_query = position_query.filter_by(user_id=user_id)
    elif model == Activity:
        position_query = position_query.filter_by(destination_id=destination_id)

    #Checken, ob erforderlicher Titel übergeben wurde
    if 'title' not in data or not data['title'] or data['title'] == '':
        return jsonify({'error': 'Title is required'}), 400

    #Neue Position setzen
    highest_position = position_query.scalar()
    new_position = (highest_position + 1) if highest_position is not None else 1

    # Initialisiere das neue Objekt mit den übergebenen Daten
    new_entry = model(**data, position=new_position)

    #Objektspezifische Daten initialisieren
    if user_id:
        new_entry.user_id = user_id
    if destination_id:
        new_entry.destination_id = destination_id

    # Speichern in der Datenbank
    db.session.add(new_entry)
    db.session.commit()

    # JSON-Antwort mit den erstellten Daten zurückgeben
    response_data = {column.name: getattr(new_entry, column.name) for column in new_entry.__table__.columns}
    return jsonify({'message': f'{model.__name__} added successfully!', model.__name__.lower(): response_data}), 201
