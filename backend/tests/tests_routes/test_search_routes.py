import pytest

from tests.helpers.variables import url
from tests.test_data.search_data import search_data


@pytest.mark.parametrize('test_data', search_data)
def test_search_resources(setup_logged_in_user, test_data):
    """Test: Search string in destinations and/or activities"""

    # Use route
    search_url = f'{url}/search?query={test_data['query']}&type={test_data['type']}'
    response = setup_logged_in_user.get(search_url)
    response_data = response.json

    # Validate expected status code
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop the test if thrown error message was expected
    if response.status_code not in [200, 201]:
        assert test_data['expected_message'] in response_data['error'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'
        return

    # Check for expected number of results
    results = response_data.get('results', [])
    assert len(results) == test_data['expected_results'], f'Error: Expected length of results: {test_data['expected_results']}, but got: {len(results)}'

