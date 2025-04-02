import pytest

from app import db
from app.models import Destination
from tests.helping_variables import url
from tests.helping_functions import request_and_validate
from tests.routes_destination_data import (
    add_destination,
    get_destination,
    edit_destination,
    reorder_destinations,
    delete_destination
)

'''
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
'''
# Test edit destination
@pytest.mark.parametrize('test_data', edit_destination)
def test_edit(setup_logged_in_user, test_data):

    # Use and validate route
    response = request_and_validate(client=setup_logged_in_user, endpoint=f'destination/edit/{test_data['destination_id']}', test_data=test_data , json_method=True)
    if response.status_code not in [200, 201]:
        return

    # Check for updates in db
    destination = Destination.query.filter_by(id=1).first()
    assert destination.title == test_data['title'], f'Unexpedted Error: Destination not edited in db'
'''
# Test reorder destinations
@pytest.mark.parametrize('test_data', reorder_destinations)
def test_reorder(setup_logged_in_user, test_data):

    # Use and validate route
    response = request_and_validate(client=setup_logged_in_user, endpoint='destination/reorder', test_data=test_data)
    if response.status_code not in [200, 201]:
        return

    # Check for new order in db
    reordered_destinations = Destination.query.filter_by(user_id=1).order_by(Destination.position).all()
    reordered_ids = [dest.id for dest in reordered_destinations]
    assert reordered_ids == test_data['new_order'], f'Error! Expected: {test_data['new_order']}, but got: {reordered_ids}'

# Test delete destinations
@pytest.mark.parametrize('test_data', delete_destination)
def test_delete(setup_logged_in_user, test_data):

    # Use and validate route
    response = request_and_validate(client=setup_logged_in_user, endpoint=f'destination/delete/{test_data['destination_id']}', test_data=test_data, method='DELETE')
    if response.status_code not in [200, 201]:
        return

    # Check if destination got deleted in db
    destination = Destination.query.filter_by(user_id=test_data['destination_id']).first()
    assert destination, f'Error: Destination still found in database'
'''
