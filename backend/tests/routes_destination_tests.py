import pytest

from app import db
from app.models import User, Destination
from tests.helping_variables import url, email, username
from tests.helping_functions import request_and_validate
from tests.routes_destination_data import (
    add_destination,
    get_destination
)


# Test add destination
@pytest.mark.parametrize('test_data', add_destination)
def test_add(setup_logged_in_user, test_data):

    response = request_and_validate(setup_logged_in_user, 'destination/add', test_data, json_method=True)
    if response.status_code not in [200, 201]:
        return

    destination = Destination.query.filter_by(title=test_data['title']).first()
    assert destination is not None, f'Error: Destination not found in db'
    assert destination.id == 7, f'Error: ID expected: 4, but got: {destination.id}'
    assert destination.position == 4, f'Error: Position expected: 4, but got: {destination.position}'
    assert destination.user_id == 1, f'Error: User-ID expected: 1, but got: {destination.position}'

# Test get all destinations of user
def test_get_all(setup_logged_in_user):

    get_url = f'{url}/destination/get_all'
    response = setup_logged_in_user.get(get_url)
    response_data = response.json()

    assert response.status_code == 200, f'Unexpected Error! Status: {response.status_code}, Text: {response.text}'
    assert len(response_data) >= 0, f'Unexpected Error: No destinations found!'
    assert response_data[2]['title'] == 'Tokyo', f'Unexpected Error: Title not found!'

# Test get specific destination
@pytest.mark.parametrize('test_data', get_destination)
def test_get_destination(setup_logged_in_user, test_data):

    # Use route
    request_and_validate(client=setup_logged_in_user, endpoint=f'destination/get/{test_data['destination_id']}', test_data=test_data, json_method=True, method='GET')

