from flask import Blueprint, request, jsonify, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from app import db
from app.models import User
from app.routes.helpers import (
    is_valid_email,
    validate_password,
    send_verification_email,
    send_email,
    edit_entry,
    delete_item,
)

user_bp = Blueprint('user', __name__, url_prefix='/user')

# Route to show profile
@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    # Show profile data except for password and data that was not logged in explicitly
    user_data = {key: value for key, value in current_user.__dict__.items() if key not in ['password', 'is_email_verified'] and not key.startswith('_')}
    return jsonify(user_data), 200

# Route to edit profile
@user_bp.route('/edit', methods=['POST'])
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

@user_bp.route('/edit_email', methods=['POST'])
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

@user_bp.route('/edit_password', methods=['POST'])
@login_required
def edit_password():

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

@user_bp.route('/request_password_reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'If E-Mail exists, a reset link has been sent.'}), 200

    # Token generieren
    serializer = current_app.config['SERIALIZER']
    token = serializer.dumps(email, salt='password-reset')
    reset_url = url_for('reset_password', token=token, _external=True)

    subject = 'Reset password'
    body = f'Click the link to reset your password: {reset_url}'
    send_email(email, subject, body)

    return jsonify({'message': 'If E-Mail exists, a reset link has been sent.'}), 200

@user_bp.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    try:
        serializer = current_app.config['SERIALIZER']
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

@user_bp.route('/delete', methods=['DELETE'])
@login_required
def delete_profile():
    user_id = current_user.id
    return delete_item(User, user_id)

