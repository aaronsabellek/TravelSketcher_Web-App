import requests
import time

from werkzeug.security import generate_password_hash

from app.models import User, Destination, Activity
from app.helpers.helpers import generate_token
from tests.helpers.variables import (
    url,
    mailhog_v2,
    mailhog_v1,
    email,
    login_data_username,
    registration_base_data
)


def request_and_validate(client, endpoint, test_data, method='POST'):
    """Sends request and validates output"""

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


def clear_mailhog():
    """Clears MailHog Mailbox"""
    requests.delete(mailhog_v1)


def check_for_mail(subject):
    """Check for incoming email by subject"""

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
    """Creates test token for verification emails"""

    # Generate token
    token = generate_token(email=email, salt=salt)

    # Set token as invalid if this should be tested
    for data in test_data:
        if 'invalid_token' in data:
            token = 'invalid_token'

    return token


def login(client, login_data=login_data_username):
    """Login user"""

    login_url = f'{url}/auth/login'
    response = client.post(login_url, json=login_data)
    assert response.status_code == 200, f'Error: Login failed! Status: {response.status_code}, Text: {response.text}'

    return client


def register(client):
    """Register user"""

    register_url = f'{url}/auth/register'
    response = client.post(register_url, json=registration_base_data)
    assert response.status_code in [200, 201], f'Error: Registration failed! Status: {response.status_code}, Text: {response.text}'

    return response


def create_user(db, user_data):
    """Creates users from dummy data"""

    hashed_password = generate_password_hash(user_data['password'], method='pbkdf2:sha256')
    user = User(
        id=user_data['id'],
        username=user_data['username'],
        email=user_data['email'],
        password=hashed_password,
        city=user_data['city'],
        longitude=user_data['longitude'],
        latitude=user_data['latitude'],
        country=user_data['country'],
        currency=user_data['currency'],
        is_email_verified=user_data['is_email_verified']
    )
    db.session.add(user)
    db.session.commit()
    return user


def create_destinations_and_activities(db, destinations_data, user):
    """Creates destinations and activities from dummy data"""

    for dest_data in destinations_data:
        destination = Destination(
            id=dest_data['id'],
            title=dest_data['title'],
            country=dest_data['country'],
            position=dest_data['position'],
            user_id=user.id
        )
        db.session.add(destination)
        db.session.commit()

        for act_data in dest_data['activities']:
            activity = Activity(
                id=act_data['id'],
                title=act_data['title'],
                country=act_data['country'],
                position=act_data['position'],
                destination_id=destination.id
            )
            db.session.add(activity)
        db.session.commit()

