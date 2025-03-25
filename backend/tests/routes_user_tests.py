import requests
import time
import pytest

from app import db
from app.models import User
from app.routes.helpers import generate_verification_token
from tests.helping_functions import clear_mailhog

from tests.helping_variables import (
    url,
    mailhog_v2,
    login_data_username,
)

from tests.routes_user_data import (
    updated_profile,
    edit_data
)

'''
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
'''
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

    # Get edited user data as dict
    user = User.query.filter_by(username=test_data['username']).first()
    assert user, f'Error: User not found! Status: {response.status_code}, Text: {response.text}'
    db.session.refresh(user)
    user_data = {column.name: getattr(user, column.name) for column in User.__table__.columns}
    allowed_fields = ['username', 'city', 'longitude', 'latitude', 'country', 'currency', 'message']

    for key, value in test_data.items():
        # Check if new user data matches the input
        if key not in ['expected_status', 'expected_message', 'password']:
            assert key in allowed_fields, f'Unexpected error: Key not allowed: {key}'
            assert value == user_data[key], f'Unexpected error: Value does not match input data! Expected: {value}, got: {user_data[key]}'
        # Check that unallowed field has not been updated
        if key == 'password':
            assert user_data['password'] != test_data['password'], f'Unexpected error: Data should not have been changed: {test_data['password']}'

