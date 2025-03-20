from flask import request, jsonify, url_for
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from models import User, Destination, Activity
from app import app, db, login_manager, mail
from helpers import (
    serializer,
    models_to_list,
    is_valid_email,
    confirm_verification_token,
    send_verification_email,
    validate_password,
    send_password_change_notification,
    create_entry,
    get_entry,
    edit_entry,
    reorder_items,
    delete_item,
    search_resources
)


'''
                APIs FOR USERS
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
    try:
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
        password_validation = validate_password(password)
        if password_validation:
            return password_validation

        # Passwort verschlüsseln
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(
            **{key: data[key] for key in required_fields if key != "password"},
                        password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        send_verification_email(new_user)

        return jsonify({'message': 'Benutzer erfolgreich registriert!'}), 201

    except Exception as e:  # Allgemeine Fehlerbehandlung
        db.session.rollback()
        return jsonify({'error': 'Ein unerwarteter Fehler ist aufgetreten', 'details': str(e)}), 500

@app.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    email = confirm_verification_token(token)
    if not email:
        return jsonify({'error': 'Ungültiger oder abgelaufener Bestätigungslink!'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found!'}), 404

    if user.is_email_verified:
        return jsonify({'message': 'E-Mail has already been confirmed!'}), 200

    user.is_email_verified = True
    db.session.commit()

    return jsonify({'message': 'E-Mail confirmed successfully!'}), 200

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

    if not user:
        return jsonify({'error': 'User not found!'}), 404

    if not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Wrong password!'}), 400

    if not user.is_email_verified:
        return jsonify({'error': 'E-Mail has not been confirmed yet!'}), 403

    login_user(user)
    return jsonify({'message': 'Login erfolgreich!'}), 200

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

    # Prüfen, ob das Passwort geändert wird
    if "password" in data:
        new_password = data["password"]

        # Passwort-Validierung mit der vorhandenen Hilfsfunktion
        password_validation = validate_password(new_password)
        if password_validation:
            return password_validation

        # Neues Passwort hashen
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        data["password"] = hashed_password

    # Änderungen speichern
    response = edit_entry(User, current_user.id, data)

    # Falls das Passwort geändert wurde, eine Bestätigungs-E-Mail senden
    if "password" in data:
        send_password_change_notification(current_user.email)

    return response

@app.route('/edit_email', methods=['POST'])
@login_required
def edit_email():
    data = request.get_json()
    new_email = data.get("email")

    if not new_email:
        return jsonify({'error': 'No E-Mail found!'}), 400

    if not is_valid_email(new_email):
        return jsonify({'error': 'Wrong Email format!'}), 400

    if User.query.filter_by(email=new_email).first():
        return jsonify({'error': 'E-Mail is already taken!'}), 400

    # Temporär die neue E-Mail speichern
    current_user.temp_email = new_email
    db.session.commit()

    send_verification_email(current_user)
    return jsonify({'message': 'Verification E-Mail has been sent. Pleayse check your E-Mails.'}), 200

@app.route('/request_password_reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'If E-Mail exists, a reset link has been sent.'}), 200

    # Token generieren
    token = serializer.dumps(email, salt='password-reset')
    reset_url = url_for('reset_password', token=token, _external=True)

    # E-Mail senden
    msg = Message('Reset password', sender='your_email@example.com', recipients=[email])
    msg.body = f'Click the link to reset your password: {reset_url}'
    mail.send(msg)

    return jsonify({'message': 'If E-Mail exists, a reset link has been sent.'}), 200

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset', max_age=1800)  # 30 Min Gültigkeit
    except:
        return jsonify({'error': 'Invalid or expired Token'}), 400

    data = request.get_json()
    new_password = data.get('new_password')

    password_validation = validate_password(new_password)
    if password_validation:
        return password_validation

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
    db.session.commit()

    return jsonify({'message': 'Password updated successfully!'}), 200

@app.route('/delete_profile', methods=['DELETE'])
@login_required
def delete_profile():
    user_id = current_user.id
    return delete_item(User, user_id)

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

@app.route('/delete_destination/<int:destination_id>', methods=['DELETE'])
@login_required  # Damit der User eingeloggt sein muss
def delete_destination(destination_id):
    # Hole die Destination anhand der ID
    destination = Destination.query.filter_by(id=destination_id, user_id=current_user.id).first()

    # Wenn die Destination nicht existiert, gib einen Fehler zurück
    if destination is None:
        return jsonify({'error': 'Destination not found!'}), 404

    return delete_item(Destination, destination_id)

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

@app.route('/delete_activity/<int:activity_id>', methods=['DELETE'])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get(activity_id)

    if activity is None:
        return jsonify({'error': 'Activity not found'}), 404

    # Prüfen, ob der aktuelle Benutzer der Besitzer der zugehörigen Destination ist
    if activity.destination.user_id != current_user.id:
        return jsonify({'error': 'You are not authorized to delete this activity'}), 403

    return delete_item(Activity, activity_id)

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

