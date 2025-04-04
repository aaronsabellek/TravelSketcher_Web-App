import pytest

from werkzeug.security import check_password_hash

from app import db
from app.models import User
from tests.helping_variables import url, email, username
from tests.helping_functions import (
    request_and_validate,
    check_for_mail,
    create_test_token,
    login
)
from tests.routes_user_data import (
    new_email,
    edit_data,
    edit_email,
    reset_email,
    edit_password,
    request_password_reset,
    reset_password
)


def test_profile(setup_logged_in_user):
    """Test: Get profile of user"""

    # User profile route
    profile_url = f'{url}/user/profile'
    response = setup_logged_in_user.get(profile_url)
    assert response.status_code == 200, f'Showing profile failed! Status: {response.status_code}, Text: {response.text}'

    # Check for (un-)expected fields
    response_data = response.json()
    assert 'latitude' in response_data, f'Latitude should be shown'
    assert 'password' not in response_data, f'Password should not be shown!'
    assert 'is_email_verified' not in response_data, f'Verification status should not be shown'


@pytest.mark.parametrize('test_data', edit_data)
def test_edit(setup_logged_in_user, test_data):
    "Test: Edit profile of user"

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, 'user/edit', test_data)
    if response.status_code not in [200, 201]:
        return

    # Get edited user data from db as dict
    user = User.query.filter_by(username=test_data['username']).first()
    assert user, f'Error: User not found!'
    db.session.refresh(user)
    user_data = {column.name: getattr(user, column.name) for column in User.__table__.columns}

    # Set allowed fields
    allowed_fields = ['username', 'city', 'longitude', 'latitude', 'country', 'currency', 'message']

    # Compare user from db with input
    for key, value in test_data.items():
        # Check if new user data matches the input
        if key not in ['expected_status', 'expected_message', 'password']:
            assert key in allowed_fields, f'Unexpected error: Key not allowed: {key}'
            assert value == user_data[key], f'Unexpected error: Value does not match input data! Expected: {value}, got: {user_data[key]}'
        # Check that unallowed field has not been updated
        if key == 'password':
            assert user_data['password'] != test_data['password'], f'Unexpected error: Data should not have been changed: {test_data['password']}'


@pytest.mark.parametrize('test_data', edit_email)
def test_edit_email(setup_logged_in_user, test_data):
    """Test: Edit email of user"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, 'user/edit_email', test_data)
    if response.status_code not in [200, 201]:
        return

    # Check for email by subject
    check_for_mail('Please confirm your E-Mail')


@pytest.mark.parametrize('test_data', reset_email)
def test_reset_password(setup_database, test_data):
    """Test: Verify new email of user"""

    # Get user
    user = User.query.filter_by(username=username).first()
    user.temp_email = new_email
    db.session.commit()

    # Create test token
    email = test_data['email']
    token = create_test_token(test_data, 'email-confirmation', email=email)

    # Use and validate route
    response = request_and_validate(setup_database, f'user/verify_email/{token}', test_data, method='GET')
    if response.status_code not in [200, 201]:
        return

    # Check new email in db
    updated_user = User.query.filter_by(email=email).first()
    assert updated_user is not None, f'User with email {email} should be in db'


@pytest.mark.parametrize('test_data', edit_password)
def test_edit_password(setup_logged_in_user, test_data):
    """Test: Edit password of user"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, 'user/edit_password', test_data)
    if response.status_code not in [200, 201]:
        return

    # Check for email by subject
    check_for_mail('Confirmation: Your password has been changed')


@pytest.mark.parametrize('test_data', request_password_reset)
def test_edit_email(setup_database, test_data):
    """Test: Request password reset"""

    # Use and validate route
    response = request_and_validate(setup_database, 'user/request_password_reset', test_data)
    if response.status_code not in [200, 201]:
        return

    # Check for email by subject
    check_for_mail('Reset password')


@pytest.mark.parametrize('test_data', reset_password)
def test_reset_password(setup_database, test_data):
    """Test: Verify password reset"""

    token = create_test_token(test_data, 'reset-password') # Create test token

    # Use and validate route
    response = request_and_validate(setup_database, f'user/reset_password/{token}', test_data)
    if response.status_code not in [200, 201]:
        return

    # Check if the password is correctly updated in the database
    user = User.query.filter_by(email=email).first()
    assert user is not None, f'User with email {email} not found in the database'
    assert check_password_hash(user.password, test_data['new_password_1']), 'Password was not correctly hashed and saved in the database'


def test_delete(setup_database):
    """Test: Delete user from database"""

    client = login(setup_database) # Login

    # Delete current user
    delete_url = f'{url}/user/delete'
    response = client.delete(delete_url)
    assert response.status_code == 200, f'Error: Deletion of user failed! Status: {response.status_code}, Text: {response.text}'
    assert response.json['message'] == 'User deleted successfully!', f'Error: Unecpected message. Status: {response.status_code}, Text: {response.text}'

    # Check for user in db
    user = User.query.filter_by(username=username).first()
    assert user is None, f'Error: User can still be found in db'

