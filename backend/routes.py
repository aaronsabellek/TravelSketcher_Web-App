from flask import request, jsonify, url_for, current_app
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db, login_manager
from models import User, Destination, Activity
from helpers import (
    serializer,
    models_to_list,
    is_valid_email,
    validate_password,
    confirm_verification_token,
    send_verification_email,
    send_email,
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

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Route
@app.route('/')
def home():
    return 'Backend is active!'

# Register route
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json() # Get data

        # Check if all required fields are filled
        required_fields = ["username", "email", "password", "city", "longitude", "latitude", "country", "currency"]
        for field in required_fields:
            if not data[field] or data[field] == '':
                return jsonify({'error': 'Field(s) missing!'}), 400

        # Set variables for data that has to be checked
        username, email, password = data["username"], data["email"], data["password"]

        # Check if email has the correct format
        if not is_valid_email(email):
            return jsonify({'error': 'Wrong Email format!'}), 400

        # Check if password fits the requirements
        password_validation = validate_password(password)
        if password_validation:
            return password_validation

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username is already taken!'}), 400

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email is already taken!'}), 400

        # Hash password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Set user
        new_user = User(
            **{key: data[key] for key in required_fields if key != "password"},
                        password=hashed_password
        )

        # Add user in db
        db.session.add(new_user)
        db.session.commit()

        send_verification_email(new_user) # Send validation email

        return jsonify({'message': 'Registration was successfull! A confirmation link has been sent.'}), 201

    # Show error if route does not work as expected
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error has occured', 'details': str(e)}), 500

# Route to verify registration with email link
@app.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    try:
        # Check if verification works
        email = confirm_verification_token(token)
        if not email:
            return jsonify({'error': 'Invalid or expired verification link!'}), 400

        # Check if user with this email exists in db
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found!'}), 404

        # Check if email is already verified
        if user.is_email_verified:
            return jsonify({'message': 'E-Mail has already been confirmed!'}), 200

        # Change verification status of user for login
        user.is_email_verified = True
        db.session.commit()

        return jsonify({'message': 'E-Mail confirmed successfully!'}), 200

    # Show error if verification route does not work as expected
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error has occured', 'details': str(e)}), 500

# Login route
@app.route('/login', methods=['POST'])
def login():
    # Check if user is already logged in
    if current_user.is_authenticated:
        return jsonify({'message': 'You are logged in already'}), 200

    # Get login data
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')

    # Check if data is complete
    if not identifier or not password:
        return jsonify({'error': 'Username or password is missing!'}), 400

    # Search for identifier in db as username or email
    user = User.query.filter(
        (User.email == identifier) | (User.username == identifier)
    ).first()

    # Check if user with given identifier exists
    if not user:
        return jsonify({'error': 'User not found!'}), 404

    # Check if password is correct
    if not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Wrong password!'}), 400

    # Check if user is already verified
    if not user.is_email_verified:
        return jsonify({'error': 'E-Mail has not been confirmed yet!'}), 403

    # Login user
    login_user(user)
    return jsonify({'message': 'Login successfull!'}), 200

# Logout route
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successfull!"}), 200

# Route to show profile
@app.route('/profile', methods=['GET'])
@login_required
def get_profile():
    # Show profile data except for password and data that was not logged in explicitly
    user_data = {key: value for key, value in current_user.__dict__.items() if key not in ['password', 'is_email_verified'] and not key.startswith('_')}
    return jsonify(user_data), 200

# Route to edit profile
@app.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    # Get data
    data = request.get_json()
    new_email = data.get('email')

    for key, value in data.items():
        if not value or value == '':
            return jsonify({'error': f'{key} not found!'}), 400

    existing_username = User.query.filter_by(username=new_email).first()
    if existing_username and existing_username.id != current_user.id:
        return jsonify({'error': 'This username is already assigned'}), 400

    # Änderungen speichern
    response = edit_entry(User, current_user.id, data)
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

@app.route('/edit_password', methods=['POST'])
@login_required
def edit_password():
    try:
        data = request.get_json()

        new_password_1 = data.get('new_password_1')
        new_password_2 = data.get('new_password_2')

        if not new_password_1 or not new_password_2:
            return jsonify({'error': 'Password missing!'})

        if new_password_1 != new_password_2:
            return jsonify({'error': 'Passwords do not match!'}) # Welche error nummer?

        password_validation = validate_password(new_password_1)
        if password_validation:
            return password_validation

        hashed_password = generate_password_hash(new_password_1, method='pbkdf2:sha256')
        current_user.password = hashed_password
        db.session.commit()

        subject = "Confirmation: Your passord has been changed"
        body = "Hello,\n\n Your password has been changed successfully. If you didn't change the password by yourself, please contact us immediately.\n\nBest regards,\nYour Support-Team"

        with current_app.app_context():
            send_email(current_user.email, subject, body) # Auch Verification Mails werden hier gesendet, selbst wenn ich sie mocken will
                                                            # Warum ist das in den APIs weiter oben anders?

        #logout_user()

        return jsonify({'message': 'Password has been changed. A confirmation mail has been sent.'}), 200

    # Show error if verification route does not work as expected
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error has occured', 'details': str(e)}), 500

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

    subject = 'Reset password'
    body = f'Click the link to reset your password: {reset_url}'
    send_email(email, subject, body)

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

