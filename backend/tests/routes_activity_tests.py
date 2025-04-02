import pytest

from app.models import Activity
from tests.helping_variables import url
from tests.helping_functions import request_and_validate
from tests.routes_activity_data import (
    add_activity
)


# Test add destination
@pytest.mark.parametrize('test_data', add_activity)
def test_add(setup_logged_in_user, test_data):

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, 'activity/add', test_data, json_method=True)
    if response.status_code not in [200, 201]:
        return

    # Check for destination in db
    activity = Activity.query.filter_by(title=test_data['title']).first()
    assert activity is not None, f'Error: Activity not found in db'
    assert activity.id == 19, f'Error: ID expected: 19, but got: {activity.id}'
    assert activity.position == 6, f'Error: Position expected: 6, but got: {activity.position}'
    assert activity.destination_id == 1, f'Error: Destination-ID expected: 1, but got: {activity.position}'

