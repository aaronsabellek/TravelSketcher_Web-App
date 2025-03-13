from flask import request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import User, Destination, Activity
from helpers import create_entry
from app import app, db, login_manager


# Benutzer laden
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return "Backend ist aktiv!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # JSON-Daten vom Frontend
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Überprüfen, ob der Benutzername oder die E-Mail bereits existieren
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Benutzername bereits vergeben!'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'E-Mail bereits registriert!'}), 400

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

    # Neuen User erstellen
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Benutzer erfolgreich registriert!'}), 201

@app.route('/login', methods=['POST'])
def login():
    # Wenn der Benutzer bereits eingeloggt ist, zurück zum Dashboard
    if current_user.is_authenticated:
        return jsonify({'message': 'Bereits eingeloggt', 'redirect': '/dashboard'}), 200

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
        return jsonify({'message': 'Erfolgreich eingeloggt', 'redirect': '/dashboard'}), 200

    return jsonify({'error': 'Login fehlgeschlagen. Überprüfe deinen Benutzernamen und dein Passwort.'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Erfolgreich abgemeldet.", "success")
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET'])
@login_required
def get_profile():
    user_data = {
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'img_link': current_user.img_link
    }
    return jsonify(user_data), 200

@app.route('/edit_username', methods=['POST'])
@login_required
def edit_username():
    data = request.get_json()
    new_username = data.get('new_username')

    if not new_username:
        return jsonify({'error': 'Neuer Benutzername ist erforderlich'}), 400

    # Überprüfen, ob der Benutzername bereits vergeben ist
    existing_user = User.query.filter_by(username=new_username).first()
    if existing_user:
        return jsonify({'error': 'Dieser Benutzername ist bereits vergeben'}), 400

    # Benutzername aktualisieren
    current_user.username = new_username
    db.session.commit()

    return jsonify({'message': 'Benutzername erfolgreich aktualisiert!', 'new_username': new_username}), 200

@app.route('/add_destination', methods=['POST'])
@login_required
def add_destination():
    data = request.get_json()
    return create_entry(Destination, data, user_id=current_user.id)

@app.route('/get_destinations', methods=['GET'])
@login_required
def get_destinations():
    destinations = Destination.query.filter_by(user_id=current_user.id).all()
    print(f"Anzahl gefundener Destinationen: {len(destinations)}")

    if not destinations:
        return jsonify([])

    return jsonify([{
        'id': d.id,
        'title': d.title,
        'country': d.country,
        'img_link': d.img_link,
        'duration': d.duration,
        'tags': d.tags,
        'status': d.status,
        'months': d.months,
        'accomodation_link': d.accomodation_link,
        'accomodation_price': d.accomodation_price,
        'accomodation_text': d.accomodation_text,
        'trip_duration': d.trip_duration,
        'trip_price': d.trip_price,
        'trip_text': d.trip_text,
        'position': d.position
    } for d in destinations])

@app.route('/edit_destination/<int:destination_id>', methods=['POST'])
@login_required
def edit_destination(destination_id):
    destination = Destination.query.filter_by(id=destination_id, user_id=current_user.id).first()

    if not destination:
        return jsonify({'error': 'Destination nicht gefunden oder keine Berechtigung'}), 403

    data = request.get_json()  # JSON-Daten vom Frontend empfangen

    # Neue Werte setzen
    destination.title = data.get('title', destination.title)
    destination.country = data.get('country', destination.country)
    destination.img_link = data.get('img_link', destination.img_link)
    destination.duration = data.get('duration', destination.duration)
    destination.tags = data.get('tags', destination.tags)
    destination.status = data.get('status', destination.status)
    destination.months = data.get('months', destination.months)
    destination.accomodation_link = data.get('accomodation_link', destination.accomodation_link)
    destination.accomodation_price = data.get('accomodation_price', destination.accomodation_price)
    destination.accomodation_text = data.get('accomodation_text', destination.accomodation_text)
    destination.trip_duration = data.get('trip_duration', destination.trip_duration)
    destination.trip_price = data.get('trip_price', destination.trip_price)
    destination.trip_text = data.get('trip_text', destination.trip_text)
    destination.free_text = data.get('free_text', destination.free_text)

    db.session.commit()

    return jsonify({
        'message': 'Destination erfolgreich aktualisiert!',
        'destination': {
            'id': destination.id,
            'title': destination.title,
            'country': destination.country,
            'img_link': destination.img_link,
            'duration': destination.duration,
            'tags': destination.tags,
            'status': destination.status,
            'months': destination.months,
            'accomodation_link': destination.accomodation_link,
            'accomodation_price': destination.accomodation_price,
            'accomodation_text': destination.accomodation_text,
            'trip_duration': destination.trip_duration,
            'trip_price': destination.trip_price,
            'trip_text': destination.trip_text,
            'free_text': destination.free_text
        }
    })

@app.route('/reorder_destinations', methods=['POST'])
@login_required
def reorder_destinations():
    data = request.get_json()
    new_order = data.get("destinations")

    if not new_order:
        return jsonify({"error": "Die Liste der Destination-IDs fehlt"}), 400

    # Hole alle Destinationen des aktuellen Nutzers
    destinations = Destination.query.filter_by(user_id=current_user.id).all()
    print(f"Empfangene Destination-IDs: {new_order}")
    print(f"Verfügbare Destinationen in der Datenbank: {[d.id for d in destinations]}")
    # Erstelle ein Dictionary für schnelleren Zugriff
    destination_dict = {destination.id: destination for destination in destinations}

    # Überprüfe, ob alle angegebenen Destination-IDs existieren
    if set(new_order) != set(destination_dict.keys()):
        return jsonify({"error": "Ungültige oder fehlende Destination-IDs"}), 400

    print(f"Vor dem Umtauschen: {[destination.position for destination in destinations]}")

    for new_position, destination_id in enumerate(new_order, start=1):
        destination = destination_dict[destination_id]
        destination.position = new_position

    db.session.commit()
    return jsonify({"message": "Destinations erfolgreich umsortiert!"}), 200

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
    activities_list = [{
        'id': act.id,
        'title': act.title,
        'country': act.country,
        'duration': act.duration,
        'price': act.price,
        'activity_text': act.activity_text,
        'position': act.position,
        'status': act.status,
        'web_link': act.web_link,
        'img_link': act.img_link,
        'tags': act.tags,
        'trip_duration': act.trip_duration,
        'trip_price': act.trip_price,
        'trip_text': act.trip_text,
        'free_text': act.free_text
                        } for act in activities]

    return jsonify({'destination': destination.title, 'activities': activities_list})

@app.route('/edit_activity/<int:destination_id>/<int:activity_id>', methods=['POST'])
@login_required
def edit_activity(destination_id, activity_id):
    destination = Destination.query.filter_by(id=destination_id).first()

    if not destination:
        return jsonify({'error': 'Destination nicht gefunden'}), 404

    # Überprüfen, ob der aktuelle Benutzer der Besitzer der Destination ist
    if destination.user_id != current_user.id:
        return jsonify({'error': 'Keine Berechtigung für diese Destination'}), 403

    # Hole die Activity, die mit der ID übereinstimmt, und überprüfe, ob sie dem aktuellen Nutzer gehört
    activity = Activity.query.filter_by(id=activity_id, destination_id=destination_id).first()

    if not activity:
        return jsonify({'error': 'Activity nicht gefunden oder keine Berechtigung'}), 403

    # Empfange die JSON-Daten aus der Anfrage
    data = request.get_json()

    # Setze die neuen Werte, falls vorhanden
    activity.title = data.get('title', activity.title)
    activity.country = data.get('country', activity.country)
    activity.duration = data.get('duration', activity.duration)
    activity.price = data.get('price', activity.price)
    activity.activity_text = data.get('activity_text', activity.activity_text)
    activity.status = data.get('status', activity.status)
    activity.web_link = data.get('web_link', activity.web_link)
    activity.img_link = data.get('img_link', activity.img_link)
    activity.tags = data.get('tags', activity.tags)
    activity.trip_duration = data.get('trip_duration', activity.trip_duration)
    activity.trip_price = data.get('trip_price', activity.trip_price)
    activity.trip_text = data.get('trip_text', activity.trip_text)
    activity.free_text = data.get('free_text', activity.free_text)

    # Speichern der Änderungen in der Datenbank
    db.session.commit()

    return jsonify({
        'message': 'Activity erfolgreich aktualisiert!',
        'activity': {
            'id': activity.id,
            'title': activity.title,
            'country': activity.country,
            'duration': activity.duration,
            'price': activity.price,
            'activity_text': activity.activity_text,
            'status': activity.status,
            'web_link': activity.web_link,
            'img_link': activity.img_link,
            'tags': activity.tags,
            'trip_duration': activity.trip_duration,
            'trip_price': activity.trip_price,
            'trip_text': activity.trip_text,
            'free_text': activity.free_text
        }
    })

@app.route('/reorder_activities/<int:destination_id>', methods=['POST'])
@login_required
def reorder_activities(destination_id):
    # JSON-Daten holen
    data = request.get_json()

    new_order = data.get("activities")

    if not destination_id or not new_order:
        return jsonify({"error": "Destination ID und Activities-Liste sind erforderlich"}), 400

    # Hole alle Activities für die Destination und den Nutzer
    activities = Activity.query.filter_by(destination_id=destination_id).all()

    # Erstelle ein Dictionary mit den vorhandenen Activities für eine schnelle Zuordnung
    activity_dict = {activity.id: activity for activity in activities}
    print("Aktuelle Activities und ihre Positionen:")
    for activity in activities:
        print(f"ID: {activity.id}, Position: {activity.position}")

    # Überprüfe, ob alle angegebenen Activity-IDs existieren
    if set(map(int, new_order)) != set(activity_dict.keys()):
        return jsonify({"error": "Ungültige oder fehlende Activity-IDs"}), 400

    # Aktualisiere die Reihenfolge
    for new_position, activity_id in enumerate(new_order, start=1):
        activity = activity_dict[int(activity_id)]
        activity.position = new_position

    db.session.commit()
    return jsonify({"message": "Activities erfolgreich umsortiert!"}), 200

'''
E-Mail verification für Registration
Email bearbeiten, wenn E-Mail-verification drin ist
Passwort zurücksetzen, wenn E-Mail-verification drin ist

Einzelne Destination anzeigen
Einzelne Activity anzeigen

Destinations suchen
Activities suchen
Profil löschen
Destination löschen
Activity löschen

Hilfsfunktionen?

Wartungsmodus
'''