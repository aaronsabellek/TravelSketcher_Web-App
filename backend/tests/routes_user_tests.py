import requests
import time
import pytest

from werkzeug.security import check_password_hash

from app import db
from app.models import User
from app.routes.helpers import generate_token
from tests.helping_functions import clear_mailhog

from tests.helping_variables import (
    url,
    email,
    mailhog_v2,
    login_data_username,
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


# TEST PROFILE
def test_profile(setup_logged_in_user):

    # User profile route
    profile_url = f'{url}/user/profile'
    response = setup_logged_in_user.get(profile_url)
    assert response.status_code == 200, f'Showing profile failed! Status: {response.status_code}, Text: {response.text}'

    # Check for (un-)expected fields
    response_data = response.json()
    assert 'latitude' in response_data, f'Latitude should be shown'
    assert 'password' not in response_data, f'Password should not be shown!'
    assert 'is_email_verified' not in response_data, f'Verification status should not be shown'

# TEST EDIT
@pytest.mark.parametrize('test_data', edit_data)
def test_edit(setup_logged_in_user, test_data):

    # Use edit route
    edit_url = f'{url}/user/edit'
    response = setup_logged_in_user.post(edit_url, json=test_data)
    response_data = response.json()
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop the test if thrown error message was expected
    if response.status_code != 200:
        assert test_data['expected_message'] in response_data['error'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'
        return

    # Check for expected message
    assert test_data['expected_message'] in response_data['message'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'

    # Get edited user data drom db as dict
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

# TEST EDIT MAILS
@pytest.mark.parametrize('test_data', edit_email)
def test_edit_email(setup_logged_in_user, test_data):

    clear_mailhog() # Clear MailHog from all E-mails

    # User edit email route
    edit_url = f'{url}/user/edit_email'
    response = setup_logged_in_user.post(edit_url, json=test_data)
    response_data = response.json()
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop the test if thrown error message was expected
    if response.status_code != 200:
        assert test_data['expected_message'] in response_data['error'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'
        return

    # Check for expected message
    assert test_data['expected_message'] in response_data['message'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'

    time.sleep(1) # Wait one second for MailHog to receive the validation mail

    # Send request to MailHog
    response_email = requests.get(mailhog_v2)
    assert response_email.status_code == 200, f'Error: No Connection to MailHog! Status: {response_email.status_code}, Text: {response_email.text}'

    # Check if latest email fits the validation mail
    latest_email = response_email.json()['items'][0]
    assert latest_email, f'Error: No E-Mail found in MailHog! Status: {response_email.status_code}, Text: {response_email.text}'
    assert latest_email['Content']['Headers']['Subject'][0] == 'Please confirm your E-Mail', \
        f'Error: Subject of the latest Mail does not fit the validation mail!' \
        f'Status: {response_email.status_code}, Text: {response_email.text}'

# TEST NEW EMAIL VERIFICATION
@pytest.mark.parametrize('test_data', reset_email)
def test_reset_password(setup_database, test_data):

    user = User.query.filter_by(id=1).first()
    user.temp_email = new_email
    db.session.commit()

    email = test_data['email']

    token = generate_token(email, salt='email-confirmation')
    for data in test_data:
        if 'token' in data:
            token = 'wrong_token'

    # Use reset password route
    verify_url = f'{url}/user/verify_email/{token}'
    response = setup_database.get(verify_url)
    response_data = response.json

    # Stop test if thrown error message was expected
    if response.status_code != 200:
        assert test_data['expected_message'] in response_data['error'], f'Error: Unexpected error message. Status: {response.status_code}, Text: {response.text}'
        return

    # Check for expected message
    assert test_data['expected_message'] in response_data['message'], f'Error: Unecpected message. Status: {response.status_code}, Text: {response.text}'

    updated_user = User.query.filter_by(email=email).first()
    assert updated_user is not None, f"User with email {email} should be in DB"

# TEST EDIT PASSWORD
@pytest.mark.parametrize('test_data', edit_password)
def test_edit_password(setup_logged_in_user, test_data):

    clear_mailhog() # Clear MailHog from all E-mails

    # User edit email route
    edit_url = f'{url}/user/edit_password'
    response = setup_logged_in_user.post(edit_url, json=test_data)
    response_data = response.json()
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop the test if thrown error message was expected
    if response.status_code != 200:
        assert test_data['expected_message'] in response_data['error'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'
        return

    # Check for expected message
    assert test_data['expected_message'] in response_data['message'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'

    time.sleep(1) # Wait one second for MailHog to receive the validation mail

    # Send request to MailHog
    response_email = requests.get(mailhog_v2)
    assert response_email.status_code == 200, f'Error: No Connection to MailHog! Status: {response_email.status_code}, Text: {response_email.text}'

    # Check if latest email fits the validation mail
    latest_email = response_email.json()['items'][0]
    assert latest_email, f'Error: No E-Mail found in MailHog! Status: {response_email.status_code}, Text: {response_email.text}'
    assert latest_email['Content']['Headers']['Subject'][0] == 'Confirmation: Your password has been changed', \
        f'Error: Subject of the latest Mail does not fit the validation mail!' \
        f'Status: {response_email.status_code}, Text: {response_email.text}'

# TEST PASSWORD RESET REQUEST
@pytest.mark.parametrize('test_data', request_password_reset)
def test_edit_email(setup_database, test_data):

    clear_mailhog() # Clear MailHog from all E-mails

    # User edit email route
    edit_url = f'{url}/user/request_password_reset'
    response = setup_database.post(edit_url, json=test_data)
    response_data = response.json

    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop the test if thrown error message was expected
    if response.status_code != 200:
        assert test_data['expected_message'] in response_data['error'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'
        return

    # Check for expected message
    assert test_data['expected_message'] in response_data['message'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'

    time.sleep(1) # Wait one second for MailHog to receive the validation mail

    # Send request to MailHog
    response_email = requests.get(mailhog_v2)
    assert response_email.status_code == 200, f'Error: No Connection to MailHog! Status: {response_email.status_code}, Text: {response_email.text}'

    # Check if latest email fits the validation mail
    latest_email = response_email.json()['items'][0]
    assert latest_email, f'Error: No E-Mail found in MailHog! Status: {response_email.status_code}, Text: {response_email.text}'
    assert latest_email['Content']['Headers']['Subject'][0] == 'Reset password', \
        f'Error: Subject of the latest Mail does not fit the validation mail!' \
        f'Status: {response_email.status_code}, Text: {response_email.text}'

# TEST PASSWORD RESET
@pytest.mark.parametrize('test_data', reset_password)
def test_reset_password(setup_database, test_data):

    # Generate token
    token = generate_token(email, salt='reset-password')

    # Set token as invalid if this should be tested
    for data in test_data:
        if 'invalid_token' in data:
            token = 'invalid_token'

    # Use reset password route
    reset_url = f'{url}/user/reset_password/{token}'
    response = setup_database.post(reset_url, json=test_data)
    response_data = response.json

    # Check status code
    assert response.status_code == test_data['expected_status'], f'Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop the test if thrown error message was expected
    if response.status_code != 200:
        assert test_data['expected_message'] in response_data['error'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'
        return

    # Check for expected message
    assert test_data['expected_message'] in response_data['message'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'

    # Check if the password is correctly updated in the database
    user = User.query.filter_by(email=email).first()
    assert user is not None, f'User with email {email} not found in the database'
    assert check_password_hash(user.password, test_data['new_password_1']), 'Password was not correctly hashed and saved in the database'

def test_delete(setup_database):

    login_url = f'{url}/auth/login'
    login_response = setup_database.post(login_url, json=login_data_username)
    assert login_response.status_code == 200, f'Error: Login failed! Status: {login_response.status_code}, Text: {login_response.text}'

    delete_url = f'{url}/user/delete'
    response = setup_database.delete(delete_url)

    assert response.status_code == 200, f'Error: Deletion of user failed! Status: {response.status_code}, Text: {response.text}'
    assert response.json['message'] == 'User deleted successfully', f'Error: Unecpected message. Status: {response.status_code}, Text: {response.text}'

