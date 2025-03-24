from flask import Blueprint, jsonify, request, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from app.models import User

from app.routes.helpers import (
    is_valid_email,
    validate_password,
    confirm_verification_token,
    send_verification_email,
)


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Route
@auth_bp.route('/')
def home():
    return 'Backend is active!'

# Register route
@auth_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    # Check if all required fields are filled
    required_fields = ['username', 'email', 'password', 'city', 'longitude', 'latitude', 'country', 'currency']
    for field in required_fields:
        if not data[field] or data[field] == '':
            return jsonify({'error': 'Field(s) missing!'}), 400

    # Set variables for data that has to be checked
    username, email, password = data['username'], data['email'], data['password']

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
        **{key: data[key] for key in required_fields if key != 'password'},
                    password=hashed_password
    )

    # Add user in db
    db.session.add(new_user)
    db.session.commit()

    send_verification_email(new_user) # Send validation email

    return jsonify({'message': 'Registration was successfull! A confirmation link has been sent.'}), 201

# Verification route
@auth_bp.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):

    # Verify email
    email = confirm_verification_token(token)

    # Check if varification has worked
    if not email:
        return jsonify({'error': 'Invalid or expired token!'}), 400

    # Check if user with this email exists in db
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found!'}), 404

    # Check if email is already verified
    if user.is_email_verified == True:
        return jsonify({'message': 'E-Mail has already been confirmed!'}), 200

    # Change verification status of user in db
    user.is_email_verified = True
    db.session.commit()

    return jsonify({'message': 'E-Mail confirmed successfully!'}), 200

# Resend verification route
@auth_bp.route('/resend_verification', methods=['POST'])
def resend_verification():

    data = request.get_json()
    email = data.get('email')

    # Check if user exists in db
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found!'}), 404

    # Check if user is already verified
    if user.is_email_verified:
        return jsonify({'message': 'E-Mail is already verified!'}), 200

    # Send new verification mail
    send_verification_email(user)
    return jsonify({'message': 'New verification link has been sent!'}), 200

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    # Check if user is already logged in
    if current_user.is_authenticated:
        return jsonify({'message': 'You are logged in already'}), 200

    # Get login data
    data = request.get_json()
    identifier, password = data.get('identifier'), data.get('password')

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
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successfull!"}), 200