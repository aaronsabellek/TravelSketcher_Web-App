from flask import jsonify
from sqlalchemy import func, String, Text
from flask_login import logout_user

import re
from app import app, db
from models import User, Destination, Activity


def model_to_dict(model):
    """Wandelt ein SQLAlchemy-Objekt in ein Dictionary um."""
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}

def models_to_list(models):
    """Wandelt eine Liste von SQLAlchemy-Objekten in eine Liste von Dictionaries um."""
    return [model_to_dict(model) for model in models]


def is_valid_email(email):
    # Regulärer Ausdruck für eine einfache E-Mail-Validierung
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Überprüft, ob die E-Mail dem regulären Ausdruck entspricht
    return bool(re.match(regex, email))

#Funktion zum Hinzufügen eines Objekts zur Datenbank (Destination oder Activity)
def create_entry(model, data, user_id=None, destination_id=None):

    try:
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

    except Exception as e:  # Unerwartete Fehler
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

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

def edit_entry(model, entry_id, data):
    """ Bearbeitet einen bestehenden Datenbankeintrag """
    try:
        query = model.query.filter_by(id=entry_id)
        entry = query.first()

        # Falls kein Eintrag gefunden oder keine Berechtigung, Fehler zurückgeben
        if not entry:
            return jsonify({'error': f'{model.__name__} nicht gefunden oder keine Berechtigung'}), 403

        # Erlaubte Felder abrufen
        allowed_fields = {column.name for column in model.__table__.columns}

        # Nur erlaubte Werte aktualisieren
        for key, value in data.items():
            if key in allowed_fields:
                setattr(entry, key, value)

        # Änderungen speichern
        db.session.commit()

        return jsonify({'message': f'{model.__name__} erfolgreich aktualisiert!', model.__name__.lower(): model_to_dict(entry)})

    except Exception as e:  # Unerwarteter Fehler
        db.session.rollback()
        return jsonify({'error': 'Ein unerwarteter Fehler ist aufgetreten', 'details': str(e)}), 500

def reorder_items(model, filter_by, new_order, item_name):
    """Allgemeine Funktion zur Neuanordnung von Objekten in einer bestimmten Reihenfolge."""
    try:
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

    except Exception as e:  # Unerwarteter Fehler
        db.session.rollback()
        return jsonify({'error': 'Ein unerwarteter Fehler ist aufgetreten', 'details': str(e)}), 500

def delete_item(model, item_id):
    """Allgemeine Funktion zum Löschen von Entitäten (Destinations oder Activities)"""
    item = model.query.get(item_id)

    try:
        db.session.delete(item)
        db.session.commit()

        if model == User:
            logout_user()

        return jsonify({'message': f'{model.__name__} deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Fehler beim Löschen der {model.__name__.lower()} {item_id}: {e}")
        return jsonify({'error': f'Fehler beim Löschen der {model.__name__.lower()}. Bitte später erneut versuchen.'}), 500

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

