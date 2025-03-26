import requests
import time
import pytest

from app import db
from app.models import User
from app.routes.helpers import generate_token
from tests.helping_functions import clear_mailhog

from tests.helping_variables import (
    url,
    mailhog_v2,
    login_data_username,
)

from tests.routes_auth_data import (
    registration_data,
    registration_base_data,
    verification_data,
    resend_verification_data,
    login_data
)


# TEST REGISTRATION
@pytest.mark.parametrize('test_data', registration_data)
def test_registration(setup_database, test_data):

    clear_mailhog() # Clear MailHog from all E-mails

    # Use registration route
    register_url = f'{url}/auth/register'
    response = setup_database.post(register_url, json=test_data)
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop the test if thrown error message was expected
    if response.status_code not in [200, 201]:
        assert test_data['expected_message'] in response.json['error'], f'Error: Unexpected error message. Status: {response.status_code}, Text: {response.text}'
        return

    # Check for expected message
    assert test_data['expected_message'] in response.json['message'], f'Error: Unecpected message. Status: {response.status_code}, Text: {response.text}'

    time.sleep(1) # Wait one second for MailHog to receive the validation mail

    # Check db for user entry
    user = User.query.filter(
        (User.username == test_data['username']) | (User.email == test_data['email'])
    ).first()
    assert user is not None, f'Error: User has not been found in database: {test_data['username']}'

    # Send request to MailHog
    response = requests.get(mailhog_v2)
    assert response.status_code == 200, f'Error: No Connection to MailHog! Status: {response.status_code}, Text: {response.text}'

    # Check if latest email fits the validation mail
    latest_email = response.json()['items'][0]
    assert latest_email, f'Error: No E-Mail found in MailHog! Status: {response.status_code}, Text: {response.text}'
    assert latest_email['Content']['Headers']['Subject'][0] == 'Please confirm your E-Mail', \
        f'Error: Subject of the latest Mail does not fit the validation mail!' \
        f'Status: {response.status_code}, Text: {response.text}'

# TEST EMAIL VERIFICATION
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

    # Generate working verification token, except a wrong token is tested
    token = generate_token(email, salt='account-verification')
    for data in test_data:
        if 'token' in data:
            token = 'wrong_token'

    # Verify email with token
    verify_url = f'{url}/auth/verify_email/{token}'
    response = setup_database.get(verify_url)
    response_data = response.json
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop test if thrown error message was expected
    if response.status_code != 200:
        assert test_data['expected_message'] in response_data['error'], f'Error: Unexpected error message. Status: {response.status_code}, Text: {response.text}'
        return

    # Check for expected message
    assert test_data['expected_message'] in response_data['message'], f'Error: Unecpected message. Status: {response.status_code}, Text: {response.text}'

    # If email has not been already confirmed before, check if it is confirmed now
    if not 'E-Mail has already been confirmed!' in response.text:
        assert user.is_email_verified == True, f'Error: User still not verified in database! Status: {response.status_code}, Text: {response.text}'

# TEST RESEND VERIFICATION MAIL
@pytest.mark.parametrize('test_data', resend_verification_data)
def test_resend_verification(setup_database, test_data):

    # Register user in db
    register_url = f'{url}/auth/register'
    register_response = setup_database.post(register_url, json=registration_base_data)
    assert register_response.status_code in [200, 201], f'Error: Registration failed! Status: {register_response.status_code}, Text: {register_response.text}'

    clear_mailhog() # Clear MailHog from all E-mails

    # Resend verification email
    resend_url = f'{url}/auth/resend_verification'
    response = setup_database.post(resend_url, json=test_data)
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop test if thrown error message was expected
    if response.status_code not in [200, 201]:
        assert test_data['expected_message'] in response.json['error'], f'Error: Unexpected error message. Status: {response.status_code}, Text: {response.text}'
        return

    # Check for expected message
    assert test_data['expected_message'] in response.json['message'], f'Error: Unecpected message. Status: {response.status_code}, Text: {response.text}'

    # Stop test if user has already been verified
    if 'E-Mail is already verified!' in response.text:
        return

    # Send request to MailHog
    response = requests.get(mailhog_v2)
    assert response.status_code == 200, f'Error: No Connection to MailHog! Status: {response.status_code}, Text: {response.text}'

    # Check if latest email fits the validation mail
    latest_email = response.json()['items'][0]
    assert latest_email, f'Error: No E-Mail found in MailHog! Status: {response.status_code}, Text: {response.text}'
    assert latest_email['Content']['Headers']['Subject'][0] == 'Please confirm your E-Mail', \
        f'Error: Subject of the latest Mail does not fit the validation mail!' \
        f'Status: {response.status_code}, Text: {response.text}'

# TEST LOGIN
@pytest.mark.parametrize('test_data', login_data)
def test_login(setup_database, test_data):

    login_url = f'{url}/auth/login'
    login_data = test_data

    # Get user with login data
    identifier = test_data['identifier']
    user = User.query.filter(
        (User.email == identifier) | (User.username == identifier)
    ).first()

    for data in login_data:
        # Log user already in if this should be tested
        if 'already_logged' in data:
            setup_database.post(login_url, json=login_data)
        # Set verification status of user to False if this should be tested
        if 'already_confirmed' in data:
            user.is_email_verified = False
            db.session.commit()

    # Login user
    response = setup_database.post(login_url, json=login_data)
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Check whether (error-)messages fit the expected output
    if response.status_code == 200:
        assert test_data['expected_message'] in response.json['message'], f'Error: Unecpected message. Status: {response.status_code}, Text: {response.text}'
    else:
        assert test_data['expected_message'] in response.json['error'], f'Error: Unexpected error message. Status: {response.status_code}, Text: {response.text}'

# TEST LOGOUT
def test_logout(setup_database):

    login_url = f'{url}/auth/login'
    logout_url = f'{url}/auth/logout'

    # Login
    login_response = setup_database.post(login_url, json=login_data_username)
    assert login_response.status_code == 200, f'Error: Login failed! Status: {login_response.status_code}, Text: {login_response.text}'

    # Logout
    response = setup_database.post(logout_url)
    assert response.status_code == 200, f'Error: Logout failed! Status: {login_response.status_code}, Text: {login_response.text}'
    assert response.json['message'] == 'Logout successfull!', f'Error: Unecpected message. Status: {response.status_code}, Text: {response.text}'

