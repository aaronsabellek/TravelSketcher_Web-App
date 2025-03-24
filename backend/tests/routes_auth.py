import requests
from app.models import User, Destination, Activity
from app import db, mail
from unittest.mock import patch
import time
import pytest

from app.routes.helpers import generate_verification_token, send_verification_email

from .helping_variables import (
    url,
    mailhog_v2,
    dummy_data,
    registration_data,
    verification_data,
    updated_password,
    login_data_username,
    login_data_email,
    updated_profile_data,
    destination_data,
    activity_data,
)

from .helping_functions import (
    clear_mailhog,
    login,
    logout,
    get_profile_data,
    add_item,
    get_and_check_response,
    get_resource,
    edit_item,
    reorder_items
)

@pytest.mark.parametrize('test_data', registration_data)
def test_registration(setup_database, test_data):

    clear_mailhog() # Clear MailHog from all E-mails

    # Set up variables
    register_url = f'{url}/auth/register'

    # Use registration route
    response = setup_database.post(register_url, json=test_data)
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop the test if thrown error message was expected
    if response.status_code not in [200, 201]:
        assert test_data['expected_message'] in response.json['error']
        return

    # Check for expected message
    assert test_data['expected_message'] in response.json['message']

    time.sleep(1) # Wait one second for MailHog to receive the validation mail

    # Check db for user entry
    user = User.query.filter(
        (User.username == test_data['username']) | (User.email == test_data['email'])
    ).first()
    assert user is not None, f'Error: User has not been found in database: {test_data['username']}'

    # Send request to MailHog
    response = requests.get(mailhog_v2)
    assert response.status_code == 200, f'Error: No Connection to MailHog! Status: {response.status_code}, Text: {response.text}'

    # Check if latest email fits the validation mail of the register route
    latest_email = response.json()['items'][0]
    assert latest_email, f'Error: No E-Mail found in MailHog! Status: {response.status_code}, Text: {response.text}'
    assert latest_email['Content']['Headers']['Subject'][0] == 'Please confirm your E-Mail', \
        f'Error: Subject of the latest Mail does not fit the validation mail!' \
        f'Status: {response.status_code}, Text: {response.text}'

# TEST OF EMAIL VERIFICATION ROUTE
@pytest.mark.parametrize('test_data', verification_data)
def test_verifify_email(setup_database, test_data):

    # Get email and user from data
    email = test_data['email']
    user = User.query.filter_by(email=email).first()

    # Set verification status of the user in db to False, except a True status is tested
    if user and test_data['is_email_verified'] == False:
        user.is_email_verified = False
        db.session.commit()

    # Generate working verification token, except a wrong token is tested
    token = generate_verification_token(email)
    if test_data['token'] == False:
        token = "wrong_token"

    # Verify email with token
    verify_url = f'{url}/auth/verify_email/{token}'
    response = setup_database.get(verify_url)
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop test if thrown error message was expected
    if response.status_code != 200:
        assert test_data['expected_message'] in response.json['error']
        return

    # Check for expected message
    assert test_data['expected_message'] in response.json['message']

    # If email has not been already confirmed before, check if it is confirmed now
    if not 'E-Mail has already been confirmed!' in response.text:
        assert user.is_email_verified == True, f'Error: User still not verified in database! Status: {response.status_code}, Text: {response.text}'

