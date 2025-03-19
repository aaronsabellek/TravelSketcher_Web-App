from flask import request, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import User, Destination, Activity
from app import app, db, login_manager
from helpers import (
    models_to_list,
    is_valid_email,
    create_entry,
    get_entry,
    edit_entry,
    reorder_items,
    search_resources
)


'''
                APIs FOR USER
'''

# Benutzer laden
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return "Backend ist aktiv!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ["username", "email", "password", "city", "longitude", "latitude", "country", "currency"]

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Fehlende Eingaben!'}), 400

    username, email, password = data["username"], data["email"], data["password"]

    # Überprüfen, ob der Benutzername oder die E-Mail bereits existieren
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Benutzername bereits vergeben!'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'E-Mail bereits registriert!'}), 400

    if not is_valid_email(email):
        return jsonify({'error': 'Wrong Email format!'}), 400

    # Passwort-Checks
    if len(password) < 8:
        return jsonify({'error': 'Passwort muss mindestens 8 Zeichen lang sein!'}), 400
    if not any(i.isdigit() for i in password):
        return jsonify({'error': 'Passwort muss mindestens eine Zahl enthalten!'}), 400
    if not any(i.isalpha() for i in password):
        return jsonify({'error': 'Passwort muss mindestens einen Buchstaben enthalten!'}), 400
    if not any(not i.isalnum() for i in password):
        return jsonify({'error': 'Passwort muss mindestens ein Sonderzeichen enthalten!'}), 400

    # Passwort verschlüsseln
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(
        **{key: data[key] for key in required_fields if key != "password"},
                    password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Benutzer erfolgreich registriert!'}), 201

@app.route('/login', methods=['POST'])
def login():
    # Wenn der Benutzer bereits eingeloggt ist, zurück zum Dashboard
    if current_user.is_authenticated:
        return jsonify({'message': 'Bereits eingeloggt'}), 200

    # JSON-Daten aus der Anfrage
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'error': 'Benutzername oder Passwort fehlt!'}), 400

    # Suche nach Benutzer, entweder nach E-Mail oder Benutzername
    user = User.query.filter(
        (User.email == identifier) | (User.username == identifier)
    ).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Erfolgreich eingeloggt'}), 200

    return jsonify({'error': 'Login fehlgeschlagen. Überprüfe deinen Benutzernamen und dein Passwort.'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Erfolgreich abgemeldet"}), 200

@app.route('/profile', methods=['GET'])
@login_required
def get_profile():
    user_data = {key: value for key, value in current_user.__dict__.items() if key != 'password' and not key.startswith('_')}
    return jsonify(user_data), 200

@app.route('/edit_profile', methods=['POST'])
@login_required
def edit_username():
    data = request.get_json()

    existing_username = User.query.filter_by(username=data['username']).first()
    if existing_username and existing_username.id != current_user.id:
        return jsonify({'error': 'Dieser Benutzername ist bereits vergeben'}), 400

    existing_email = User.query.filter_by(email=data['email']).first()
    if existing_email and existing_email.id != current_user.id:
        return jsonify({'error': 'Diese Email ist bereits vergeben'}), 400

    return edit_entry(User, current_user.id, data)

'''
                APIs FOR DESTINATIONS
'''

@app.route('/add_destination', methods=['POST'])
@login_required
def add_destination():
    data = request.get_json()
    return create_entry(Destination, data, user_id=current_user.id)

@app.route('/get_destinations', methods=['GET'])
@login_required
def get_destinations():
    destinations = Destination.query.filter_by(user_id=current_user.id).all()

    return jsonify(models_to_list(destinations))

@app.route('/get_destination/<int:destination_id>', methods=['GET'])
@login_required
def get_destination(destination_id):
    destination_data, status_code = get_entry(Destination, destination_id)

    if status_code != 200:
        return jsonify({'error': 'Destination nicht gefunden oder nicht berechtigt'}), status_code

    return jsonify(destination_data), status_code

@app.route('/edit_destination/<int:destination_id>', methods=['POST'])
@login_required
def edit_destination(destination_id):
    data = request.get_json()

    # Sicherstellen, dass die Destination dem aktuellen Benutzer gehört
    destination = Destination.query.filter_by(id=destination_id, user_id=current_user.id).first()

    if not destination:
        return jsonify({'error': 'Destination nicht gefunden oder nicht berechtigt'}), 403

    return edit_entry(Destination, destination_id, data)

@app.route('/reorder_destinations', methods=['POST'])
@login_required
def reorder_destinations():
    data = request.get_json()
    new_order = data.get("destinations")
    return reorder_items(Destination, {"user_id": current_user.id}, new_order, "destinations")


'''
                APIs FOR ACTIVITIES
'''

@app.route('/add_activity', methods=['POST'])
@login_required
def add_activity():
    data = request.get_json()
    destination_id = data.get('destination_id')

    if not Destination.query.get(destination_id):
        return jsonify({'error': 'Destination not found'}), 404

    return create_entry(Activity, data, destination_id=destination_id)

@app.route('/get_activities/<int:destination_id>', methods=['GET'])
@login_required
def get_activities(destination_id):

    destination = Destination.query.get(destination_id)

    if not destination:
        return jsonify({'error': 'Destination not found'}), 404

    # Überprüfen, ob der aktuelle Benutzer der Besitzer der Destination ist
    if destination.user_id != current_user.id:
        return jsonify({'error': 'Keine Berechtigung für diese Destination'}), 403

    activities = Activity.query.filter_by(destination_id=destination_id).all()

    return jsonify({
        'destination': destination.title,
        'activities': models_to_list(activities)  # Kein manuelles Mapping mehr nötig!
    })

@app.route('/get_activity/<int:activity_id>', methods=['GET'])
@login_required
def get_activity(activity_id):
    # Benutze die Hilfsfunktion, um die Activity-Daten zu holen
    activity_data, status_code = get_entry(Activity, activity_id)

    if status_code != 200:
        return jsonify({'error': 'Activity nicht gefunden'}), status_code

    # Sicherstellen, dass der Benutzer Zugriff auf die Activity hat
    activity = Activity.query.get(activity_id)
    if activity.destination.owner.id != current_user.id:
        return jsonify({'error': 'Nicht autorisiert'}), 403

    return jsonify(activity_data), status_code

@app.route('/edit_activity/<int:activity_id>', methods=['POST'])
@login_required
def edit_activity(activity_id):
    data = request.get_json()
    activity = Activity.query.get(activity_id)

    # Stelle sicher, dass der Nutzer berechtigt ist, die Activity zu bearbeiten
    if activity.destination.owner.id != current_user.id:
        return jsonify({'error': 'Nicht autorisiert'}), 403

    return edit_entry(Activity, activity_id, data)

@app.route('/reorder_activities/<int:destination_id>', methods=['POST'])
@login_required
def reorder_activities(destination_id):
    data = request.get_json()
    new_order = data.get("activities")
    return reorder_items(Activity, {"destination_id": destination_id}, new_order, "activities")

'''
                APIs FOR DESTINATIONS AND ACTIVITIES
'''

@app.route('/search', methods=['GET'])
@login_required
def search():
    search_query = request.args.get('search_query')  # Der Suchtext
    resource_type = request.args.get('resource_type')  # 'destination', 'activity' oder 'both' für beide

    if not search_query:
        return jsonify({'error': 'Suchtext ist erforderlich'}), 400

    # Felder, die wir nicht durchsuchen wollen (ID, Position und Beziehungen)
    exclude_fields = ['id', 'position', 'user_id', 'destination_id']  # Anpassbar je nach Bedarf

    results_data = []

    # Wenn nur 'destination' angegeben ist
    if resource_type == 'destination' or resource_type == 'both' or not resource_type:
        results_data.extend(search_resources(Destination, search_query, exclude_fields))

    # Wenn nur 'activity' angegeben ist
    if resource_type == 'activity' or resource_type == 'both' or not resource_type:
        results_data.extend(search_resources(Activity, search_query, exclude_fields))

    return jsonify(results=results_data), 200


'''
create_db.py löschen
Tests erweitern um Fälle, in denen falsche Daten eingegeben werden?

Profil löschen
Destination löschen
Activity löschen

Wartungsmodus

E-Mail verification für Registration
Email bearbeiten, wenn E-Mail-verification drin ist
Passwort zurücksetzen, wenn E-Mail-verification drin ist

Tests mit Pytest gründlich überarbeiten

Frontend braucht API zu geonames, um Längen- und Breitengrad zu validieren und Städtenamen für spätere Links zu validieren
Frontend braucht API zu AI, die bestimmte Felder selbstständig ausfüllt und destinations/activities selbst vorschlägt
Frontend braucht API zu Restcountries, um currency zu bestimmen, die später in Preis-Icons dargestellt wird
Frontend braucht Direktlinks zu externen Anbietern, die nach Funktion gegliedert sind:
    Booking, AirBnB
    Rome2Rio, Google Maps Routes
    TripAdvisor
'''