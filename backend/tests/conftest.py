import pytest

from app import create_app, db
from tests.helpers.functions import create_user, create_destinations_and_activities
from tests.helpers.variables import (
    url,
    user,
    second_user,
    destinations,
    second_destinations,
    login_data_username,
)


@pytest.fixture(scope='function')
def setup_database():
    """Fixture to setup the test database"""

    # Set application context
    app = create_app()
    with app.app_context():

        # Drop and create new database
        db.drop_all()
        db.create_all()

        # Create main user and secondary user
        main_user = create_user(db, user)
        secondary_user = create_user(db, second_user)

        # Create destinations and activities for users
        create_destinations_and_activities(db, destinations, main_user)
        create_destinations_and_activities(db, second_destinations, secondary_user)

        # Return test client
        with app.test_client() as client:
            yield client

        # Remove all data
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def setup_logged_in_user(setup_database):
    """Fixture to setup test database, login user and return request session"""

    # Create client
    client = setup_database

    # Login user
    login_url = f'{url}/auth/login'
    response_login = client.post(login_url, json=login_data_username)
    assert response_login.status_code == 200, f'Login failed! Status: {response_login.status_code}, Text: {response_login.text}'

    # Return client
    yield client

    # Logout user
    logout_url = f'{url}/auth/logout'
    response_logout = client.post(logout_url)
    assert response_logout.status_code == 200, f'Error: Logout failed! Status: {response_logout.status_code}, Text: {response_logout.text}'

