import requests
import time

from app.helpers.helpers import generate_token
from tests.helping_variables import (
    url,
    mailhog_v2,
    mailhog_v1,
    email,
    login_data_username,
    registration_base_data
)


# Clear MailHog mailbox
def clear_mailhog():
    requests.delete(mailhog_v1)

# Send request and validate output
def request_and_validate(client, endpoint, test_data, method='POST', json_method=None):

    # Set url
    response_url = f'{url}/{endpoint}'

    # Use route
    if method == 'GET':
        response = client.get(response_url)
    elif method == 'DELETE':
        response = client.delete(response_url)
    else:
        response = client.post(response_url, json=test_data)

    # Set response data
    if callable(response.json):
        response_data = response.json()
    else:
        response_data = response.json

    # Check for expected status
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop the test if thrown error message was expected
    if response.status_code not in [200, 201]:
        assert test_data['expected_message'] in response_data['error'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'
        return response

    # Check for expected message if there is one
    if 'message' in response_data:
        assert test_data['expected_message'] in response_data['message'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'

    return response

# Check for incoming Mail by subject
def check_for_mail(subject):

    time.sleep(1) # Wait one second for MailHog to receive the validation mail

    # Send request to MailHog
    response = requests.get(mailhog_v2)
    assert response.status_code == 200, f'Error: No Connection to MailHog! Status: {response.status_code}, Text: {response.text}'

    # Check if latest email fits the validation mail
    latest_email = response.json()['items'][0]
    assert latest_email, f'Error: No E-Mail found in MailHog! Status: {response.status_code}, Text: {response.text}'
    assert latest_email['Content']['Headers']['Subject'][0] == subject, \
        f'Error: Subject of the latest Mail does not fit the validation mail!' \
        f'Status: {response.status_code}, Text: {response.text}'

    clear_mailhog() # Clear MailHog from all E-mails

    return response

def create_test_token(test_data, salt, email=email):

    # Generate token
    token = generate_token(email=email, salt=salt)

    # Set token as invalid if this should be tested
    for data in test_data:
        if 'invalid_token' in data:
            token = 'invalid_token'

    return token

# Login user
def login(client, login_data=login_data_username):

    login_url = f'{url}/auth/login'
    response = client.post(login_url, json=login_data)
    assert response.status_code == 200, f'Error: Login failed! Status: {response.status_code}, Text: {response.text}'

    return client

# Register user
def register(client):

    register_url = f'{url}/auth/register'
    response = client.post(register_url, json=registration_base_data)
    assert response.status_code in [200, 201], f'Error: Registration failed! Status: {response.status_code}, Text: {response.text}'

    return response

