from flask import request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import User, Destination, Activity
from app import app, db, login_manager


# Benutzer laden
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return "Backend ist aktiv!"


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    destinations = Destination.query.filter_by(user_id=current_user.id).order_by(Destination.position).all()

    destinations_list = [{
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
        'free_text': d.free_text
    } for d in destinations]

    return jsonify({'destinations': destinations_list})

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
    new_username = request.form.get('new_username')

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
    if request.method == 'POST':
        # Formulardaten abrufen
        title = request.form['title']
        country = request.form.get('country')
        img_link = request.form.get('img_link')
        duration = request.form.get('duration')
        tags = request.form.get('tags')
        status = request.form.get('status')
        months = request.form.get('months')
        accomodation_link = request.form.get('accomodation_link')
        accomodation_price = request.form.get('accomodation_price')
        accomodation_text = request.form.get('accomodation_text')
        trip_duration = request.form.get('trip_duration')
        trip_price = request.form.get('trip_price')
        trip_text = request.form.get('trip_text')
        free_text = request.form.get('free_text')

        # Setze Position
        highest_position = db.session.query(db.func.max(Destination.position)).filter_by(user_id=current_user.id).scalar()
        new_position = (highest_position + 1) if highest_position is not None else 1

        # Erstelle eine neue Destination
        new_destination = Destination(
            title=title,
            country=country,
            img_link=img_link,
            duration=duration,
            tags=tags,
            status=status,
            months=months,
            accomodation_link=accomodation_link,
            accomodation_price=accomodation_price,
            accomodation_text=accomodation_text,
            trip_duration=trip_duration,
            trip_price=trip_price,
            trip_text=trip_text,
            free_text=free_text,
            position=new_position,
            user_id=current_user.id
        )

        db.session.add(new_destination)
        db.session.commit()

        # Gib die hinzugefügte Destination als JSON zurück
        return jsonify({
            'message': 'Destination added successfully!',
            'destination': {
                'id': new_destination.id,
                'title': new_destination.title,
                'country': new_destination.country,
                'img_link': new_destination.img_link,
                'duration': new_destination.duration,
                'tags': new_destination.tags,
                'status': new_destination.status,
                'months': new_destination.months,
                'accomodation_link': new_destination.accomodation_link,
                'accomodation_price': new_destination.accomodation_price,
                'accomodation_text': new_destination.accomodation_text,
                'trip_duration': new_destination.trip_duration,
                'trip_price': new_destination.trip_price,
                'trip_text': new_destination.trip_text,
                'free_text': new_destination.free_text,
                'position': new_destination.position,
                'user_id': new_destination.user_id
            }
        }), 201

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

        # Ausgabe für Debugging-Zwecke
        print("Destination ID:", destination_id)
        print("Neue Position:", destination.position)

    db.session.commit()
    return jsonify({"message": "Destinations erfolgreich umsortiert!"}), 200

@app.route('/add_activity', methods=['POST'])
@login_required
def add_activity():
    # Formulardaten holen
    title = request.form['title']

    country = request.form.get('country')
    duration = request.form.get('duration')
    price = request.form.get('price')
    activity_text = request.form.get('activity_text')
    status = request.form.get('status')
    web_link = request.form.get('web_link')
    img_link = request.form.get('img_link')
    tags = request.form.get('tags')
    trip_duration = request.form.get('trip_duration')
    trip_price = request.form.get('trip_price')
    trip_text = request.form.get('trip_text')
    free_text = request.form.get('free_text')

    destination_id = request.form['destination_id']

    # Überprüfen, ob die Destination existiert
    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({'error': 'Destination not found'}), 404

    highest_position = db.session.query(db.func.max(Activity.position)).filter_by(destination_id=destination_id).scalar()
    new_position = (highest_position + 1) if highest_position is not None else 1

    new_activity = Activity(title=title,
                            country=country,
                            duration=duration,
                            price=price,
                            activity_text=activity_text,
                            status=status,
                            web_link=web_link,
                            img_link=img_link,
                            tags=tags,
                            trip_duration=trip_duration,
                            trip_price=trip_price,
                            trip_text=trip_text,
                            free_text=free_text,

                            position=new_position,
                            destination_id=destination_id)

    db.session.add(new_activity)
    db.session.commit()

    return jsonify({'message': 'Activity added successfully!', 'activity': {
        'id': new_activity.id,
        'title': new_activity.title,
        'country': new_activity.country,
        'duration': new_activity.duration,
        'price': new_activity.price,
        'activity_text': new_activity.activity_text,
        'position': new_activity.position,
        'status': new_activity.status,
        'web_link': new_activity.web_link,
        'img_link': new_activity.img_link,
        'tags': new_activity.tags,
        'trip_duration': new_activity.trip_duration,
        'trip_price': new_activity.trip_price,
        'trip_text': new_activity.trip_text,
        'free_text': new_activity.free_text,
        'destination_id': new_activity.destination_id
    }})

@app.route('/get_activities/<int:destination_id>', methods=['GET'])
@login_required
def get_activities(destination_id):
    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({'error': 'Destination not found'}), 404
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


@app.route('/reorder_activities', methods=['POST'])
@login_required
def reorder_activities():
    # Formulardaten holen
    destination_id = request.form.get("destination_id")
    new_order = request.form.getlist("activities[]")

    if not destination_id or not new_order:
        return jsonify({"error": "Destination ID und Activities-Liste sind erforderlich"}), 400

    # Hole alle Activities für die Destination und den Nutzer
    activities = Activity.query.filter_by(destination_id=destination_id, user_id=current_user.id).all()

    # Erstelle ein Dictionary mit den vorhandenen Activities für eine schnelle Zuordnung
    activity_dict = {activity.id: activity for activity in activities}

    # Überprüfe, ob alle angegebenen Activity-IDs existieren
    if set(map(int, new_order)) != set(activity_dict.keys()):
        return jsonify({"error": "Ungültige oder fehlende Activity-IDs"}), 400

    # Aktualisiere die Reihenfolge
    for index, activity_id in enumerate(new_order):
        activity_dict[int(activity_id)].number = index

    db.session.commit()
    return jsonify({"message": "Activities erfolgreich umsortiert!"}), 200

'''
E-Mail verification für Registration
Email bearbeiten, wenn E-Mail-verification drin ist
Passwort zurücksetzen, wenn E-Mail-verification drin ist

Activity bearbeiten
Destinations suchen
Activities suchen
Profil löschen
Destination löschen
Activity löschen
Wartungsmodus
'''