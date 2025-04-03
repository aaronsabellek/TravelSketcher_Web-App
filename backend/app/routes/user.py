from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app import db
from app.models import User
from app.helpers.helpers import (
    is_valid_email,
    generate_token,
    confirm_token,
    send_verification_email,
    send_email,
    update_password
)
from app.helpers.helpers_entries import(
    edit_entry,
    delete_entry
)

# Set blueprint
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Set allowed fields for user display
allowed_fields = ['username', 'city', 'longitude', 'latitude', 'country', 'currency']


@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """Gets profile of user"""

    # Show profile data except for password and data that was not logged in explicitly
    user_data = {key: value for key, value in current_user.__dict__.items() if key in allowed_fields}
    return jsonify(user_data), 200


@user_bp.route('/edit', methods=['POST'])
@login_required
def edit_profile():
    """Edits user profile"""

    # Get data
    data = request.get_json()
    new_username = data.get('username')

    # Set allowed fields
    allowed_fields = ['username', 'city', 'longitude', 'latitude', 'country', 'currency']

    # Check if every value is set
    for key, value in data.items():
        if value == '':
            return jsonify({'error': f'{key} not found!'}), 400

    # Check for '@' in username
    if '@' in new_username:
        return jsonify({'error': "'@' in username is not allowed!"}), 400

    # Check if username already exist from different user
    existing_username = User.query.filter_by(username=new_username).first()
    if existing_username and existing_username.id != current_user.id:
        return jsonify({'error': 'This username already exists!'}), 400

    return edit_entry(User, current_user.id, data, allowed_fields=allowed_fields)


@user_bp.route('/edit_email', methods=['POST'])
@login_required
def edit_email():
    """Edits email of user"""

    # Get new email
    data = request.get_json()
    new_email = data.get('email')

    # Check for new email
    if not new_email or new_email == '':
        return jsonify({'error': 'No E-Mail found!'}), 400

    # Check if email has correct format
    if not is_valid_email(new_email):
        return jsonify({'error': 'Wrong Email format!'}), 400

    # Check if email already exists in db
    if User.query.filter_by(email=new_email).first():
        return jsonify({'error': 'E-Mail is already taken!'}), 400

    # Safe new email temporarily
    current_user.temp_email = new_email
    db.session.commit()

    # Send verification mail
    send_verification_email(current_user, salt='email-confirmation')

    return jsonify({'message': 'Verification e-mail has been sent.'}), 200


@user_bp.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    """Verifies the veridication email for new email of user"""

    # Confirm token
    new_email = confirm_token(token, salt='email-confirmation')

    # Check if token is valid
    if not new_email:
        return jsonify({'error': 'Invalid or expired token'}), 400

    # Check user in db
    user = User.query.filter_by(temp_email=new_email).first()
    if not user:
        return jsonify({'error': 'Request to edit email not found'}), 404

    # Edit user email in db
    user.email = new_email
    user.temp_email = None
    db.session.commit()

    return jsonify({'message': 'Email verification successful!'}), 200


@user_bp.route('/edit_password', methods=['POST'])
@login_required
def edit_password():
    """Edits password of user"""

    # Get new passwords
    data = request.get_json()
    new_password_1 = data.get('new_password_1')
    new_password_2 = data.get('new_password_2')

    # Update password
    response, status_code = update_password(current_user, new_password_1, new_password_2)

    # Send confirmation mail after successful password update
    if status_code == 200:
        subject = 'Confirmation: Your password has been changed'
        body = "Hello,\n\n Your password has been changed successfully. If you didn't change the password by yourself, please contact us immediately.\n\nBest regards,\nYour Support-Team"
        send_email(current_user.email, subject, body)

    return response, status_code


@user_bp.route('/request_password_reset', methods=['POST'])
def request_password_reset():
    """Requests password reset if password has been forgotten"""

    # Get email
    data = request.get_json()
    email = data.get('email')

    # Check email in data
    if not email:
        return jsonify({'error': 'Email missing!'}), 400

    # Check if email is in db
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'E-Mail not found!'}), 404

    # Generate token
    token = generate_token(email, salt='reset-password')
    reset_url = f'/user/reset_token/{token}'

    # Send reset mail
    subject = 'Reset password'
    body = f'Click the link to reset your password: {reset_url}'
    send_email(email, subject, body)

    return jsonify({'message': 'A reset link has been sent.'}), 200


@user_bp.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    """Resets password if reset has been requested"""

    # Confirm token
    email = confirm_token(token, salt='reset-password', expiration=1800)  # 30 Min gültig

    # Check if token is valid
    if not email:
        return jsonify({'error': 'Invalid or expired token'}), 400

    # Check user in db
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Get new password
    data = request.get_json()
    new_password_1 = data.get('new_password_1')
    new_password_2 = data.get('new_password_2')

    # Update password in db
    return update_password(user, new_password_1, new_password_2)


@user_bp.route('/delete', methods=['DELETE'])
@login_required
def delete_profile():
    """Deletes profile from database"""

    user_id = current_user.id
    return delete_entry(User, user_id)

