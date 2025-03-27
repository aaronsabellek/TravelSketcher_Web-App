import pytest

from app import db
from app.models import User, Destination
from tests.helping_variables import url, email, username
from tests.helping_functions import request_and_validate
from tests.routes_destination_data import (
    add_destination
)


# Test add destination
@pytest.mark.parametrize('test_data', add_destination)
def test_edit(setup_logged_in_user, test_data):

    response = request_and_validate(setup_logged_in_user, 'destination/add', test_data, json_method=True)
    if response.status_code not in [200, 201]:
        return

    destination = Destination.query.filter_by(title=test_data['title']).first()
    assert destination is not None, f'Error: Destination not found in db'
    assert destination.id == 4, f'Error: ID expected: 4, but got: {destination.position}'
    assert destination.position == 4, f'Error: Position expected: 4, but got: {destination.position}'
    assert destination.user_id == 1, f'Error: User-ID expected: 1, but got: {destination.position}'

