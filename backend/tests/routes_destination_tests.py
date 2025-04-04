import pytest

from app import db
from app.models import Destination
from tests.helping_functions import request_and_validate
from tests.helping_variables import (
    url,
    user,
    user_id
)
from tests.routes_destination_data import (
    new_destination,
    add_destination,
    get_destination,
    edit_destination,
    reorder_destinations,
    delete_destination
)


@pytest.mark.parametrize('test_data', add_destination)
def test_add(setup_logged_in_user, test_data):
    """Test: Add destination to database"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, 'destination/add', test_data)
    if response.status_code not in [200, 201]:
        return

    # Check for destination in db
    destination = Destination.query.filter_by(title=test_data['title']).first()
    assert destination is not None, f'Error: Destination not found in db'
    assert destination.id == new_destination['id'], f'Error: ID expected: {new_destination['id']}, but got: {destination.id}'
    assert destination.position == 4, f'Error: Position expected: 4, but got: {destination.position}'
    assert destination.user_id == user['id'], f'Error: User-ID expected: {user['id']}, but got: {destination.destination.user_id}'


def test_get_all(setup_logged_in_user):
    """Test: Get all destinations of user"""

    # Use route
    get_url = f'{url}/destination/get_all'
    response = setup_logged_in_user.get(get_url)
    response_data = response.json()

    # Check for errors
    assert len(response_data['destinations']) >= 2, f'Unexpected Error: No destinations found!'
    assert response_data['destinations'][2]['title'] == 'Tokyo', f'Unexpected Error: Title not found!'

    # Delete all destinations from db
    Destination.query.delete()
    db.session.commit()

    # Use route again
    response = setup_logged_in_user.get(get_url)
    response_data = response.json()

    # Check for errors in case of no destinations
    assert len(response_data['destinations']) == 0, f'Unexpected Error: Still destinations in db!'
    assert response_data['message'] == 'No destinations found yet'


@pytest.mark.parametrize('test_data', get_destination)
def test_get_destination(setup_logged_in_user, test_data):
    """Test: Get specific destination"""

    # Use and validate route
    request_and_validate(setup_logged_in_user, f'destination/get/{test_data['id']}', test_data, method='GET')


@pytest.mark.parametrize('test_data', edit_destination)
def test_edit(setup_logged_in_user, test_data):
    """Test: Edit destination"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, f'destination/edit/{test_data['id']}', test_data)
    if response.status_code not in [200, 201]:
        return

    # Check for updates in db
    destination = Destination.query.filter_by(id=test_data['id']).first()
    print(destination)
    assert destination.title == test_data['title'], f'Unexpedted Error: Destination not edited in db'


@pytest.mark.parametrize('test_data', reorder_destinations)
def test_reorder(setup_logged_in_user, test_data):
    """Test: Reorder destinations of user"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, 'destination/reorder', test_data)
    if response.status_code not in [200, 201]:
        return

    # Check new order in db
    reordered_destinations = Destination.query.filter_by(user_id=user_id).order_by(Destination.position).all()
    reordered_ids = [str(dest.id) for dest in reordered_destinations]
    assert reordered_ids == test_data['new_order'], f'Error: Expected: {test_data['new_order']}, got: {reordered_ids}'


@pytest.mark.parametrize('test_data', delete_destination)
def test_delete(setup_logged_in_user, test_data):
    """Test: Delete destination"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, f'destination/delete/{test_data['destination_id']}', test_data, method='DELETE')
    if response.status_code not in [200, 201]:
        return

    # Check if destination got deleted in db
    destination = Destination.query.filter_by(id=test_data['destination_id']).first()
    assert destination is None, f'Error: Destination still found in database'

