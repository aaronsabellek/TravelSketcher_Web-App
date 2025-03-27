import pytest

from app import db
from app.models import User
from tests.helping_variables import url
from tests.helping_functions import (
    request_and_validate,
    check_for_mail,
    create_test_token,
    login,
    register
)
from tests.routes_auth_data import (
    registration_data,
    verification_data,
    resend_verification_data,
    login_data
)


# Test registration
@pytest.mark.parametrize('test_data', registration_data)
def test_registration(setup_database, test_data):

    # Use and validate route
    response = request_and_validate(client=setup_database, endpoint='auth/register', test_data=test_data)
    if response.status_code not in [200, 201]:
        return

    # Check db for user entry
    user = User.query.filter(
        (User.username == test_data['username']) | (User.email == test_data['email'])
    ).first()
    assert user is not None, f'Error: User has not been found in database: {test_data['username']}'

    check_for_mail('Please confirm your E-Mail') # Check for email by subject

# Test email verification
@pytest.mark.parametrize('test_data', verification_data)
def test_verifify_email(setup_database, test_data):

    # Get email and user from data
    email = test_data['email']
    user = User.query.filter_by(email=email).first()

    # Set verification Status to False, except a True status is tested
    verification_status = False
    for data in test_data:
        if 'is_email_verified' in data:
            verification_status = True

    if user and verification_status == False:
        user.is_email_verified = False
        db.session.commit()

    token = create_test_token(test_data, 'account-verification', email=email) # Create test token

    # Use and validate route
    response = request_and_validate(client=setup_database, endpoint=f'auth/verify_email/{token}', test_data=test_data, method='GET')
    if response.status_code not in [200, 201]:
        return

    # If email has not been already confirmed before, check if it is confirmed now
    if not 'E-Mail confirmed successfully!' in response.text:
        assert user.is_email_verified == True, f'Error: User still not verified in database! Status: {response.status_code}, Text: {response.text}'

# Test resend verification mail
@pytest.mark.parametrize('test_data', resend_verification_data)
def test_resend_verification(setup_database, test_data):

    register(setup_database) # Register with new account

    # Use and validate route
    response = request_and_validate(client=setup_database, endpoint='auth/resend_verification', test_data=test_data)
    if response.status_code not in [200, 201]:
        return

    # Stop test if user has already been verified
    if 'E-Mail is already verified!' in response.text:
        return

    check_for_mail('Please confirm your E-Mail') # Check for email by subject

# Test login
@pytest.mark.parametrize('test_data', login_data)
def test_login(setup_database, test_data):

    login_url = f'{url}/auth/login'

    # Get user with login data
    identifier = test_data['identifier']
    user = User.query.filter(
        (User.email == identifier) | (User.username == identifier)
    ).first()

    for data in test_data:
        # Log user already in if this should be tested
        if 'already_logged' in data:
            setup_database.post(login_url, json=test_data)
        # Set verification status of user to False if this should be tested
        if 'already_confirmed' in data:
            user.is_email_verified = False
            db.session.commit()

    # Login user
    response = setup_database.post(login_url, json=test_data)
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Check whether (error-)messages fit the expected output
    if response.status_code == 200:
        assert test_data['expected_message'] in response.json['message'], f'Error: Unecpected message. Status: {response.status_code}, Text: {response.text}'
    else:
        assert test_data['expected_message'] in response.json['error'], f'Error: Unexpected error message. Status: {response.status_code}, Text: {response.text}'

# Test Logout
def test_logout(setup_database):

    login(setup_database) # Login

    # Logout
    logout_url = f'{url}/auth/logout'
    response = setup_database.post(logout_url)
    assert response.status_code == 200, f'Error: Logout failed! Status: {response.status_code}, Text: {response.text}'
    assert response.json['message'] == 'Logout successfull!', f'Error: Unecpected message. Status: {response.status_code}, Text: {response.text}'

