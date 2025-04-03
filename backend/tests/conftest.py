import requests
import pytest

from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import User, Destination, Activity
from .helping_variables import url, dummy_data, login_data_username, username


@pytest.fixture(scope="function")
def setup_database():
    """Fixture to setup the test database"""

    # Set application context
    app = create_app()
    with app.app_context():

        # Drop and create new database
        db.drop_all()
        db.create_all()

        # Set hashed password
        hashed_password = generate_password_hash(dummy_data['user']['password'], method='pbkdf2:sha256')

        # Create main user in database
        user = User(
            username=dummy_data['user']['username'],
            email=dummy_data['user']['email'],
            password=hashed_password,
            city=dummy_data['user']['city'],
            longitude=dummy_data['user']['longitude'],
            latitude=dummy_data['user']['latitude'],
            country=dummy_data['user']['country'],
            currency=dummy_data['user']['currency'],
            is_email_verified=dummy_data['user']['is_email_verified']
        )
        db.session.add(user)
        db.session.commit()

        # Create second user in database
        second_user = User(
            username=dummy_data['second_user']['username'],
            email=dummy_data['second_user']['email'],
            password=hashed_password,
            city=dummy_data['second_user']['city'],
            longitude=dummy_data['second_user']['longitude'],
            latitude=dummy_data['second_user']['latitude'],
            country=dummy_data['second_user']['country'],
            currency=dummy_data['second_user']['currency'],
            is_email_verified=dummy_data['second_user']['is_email_verified']
        )
        db.session.add(second_user)
        db.session.commit()

        # Create destinations and activities of main user in database
        for destination_data in dummy_data['destinations']:
            destination = Destination(
                title=destination_data['title'],
                country=destination_data['country'],
                position=destination_data['position'],
                user_id=user.id
            )
            db.session.add(destination)
            db.session.commit()

            for activity_data in destination_data['activities']:
                activity = Activity(
                    title=activity_data['title'],
                    country=activity_data['country'],
                    position=activity_data['position'],
                    destination_id=destination.id
                )
                db.session.add(activity)

            db.session.commit()

        # Create destinations and activities of second user in database
        for second_destination_data in dummy_data['second_destinations']:
            second_destination = Destination(
                title=destination_data['title'],
                country=destination_data['country'],
                position=destination_data['position'],
                user_id=second_user.id
            )
            db.session.add(second_destination)
            db.session.commit()

            for activity_data in second_destination_data['activities']:
                activity = Activity(
                    title=activity_data['title'],
                    country=activity_data['country'],
                    position=activity_data['position'],
                    destination_id=second_destination.id
                )
                db.session.add(activity)

            db.session.commit()

        # Return test client
        with app.test_client() as client:
            yield client

        # Remove all data from database
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def setup_logged_in_user(setup_database):
    """Fixture to setup test database, login user and return request session"""

    # Create session for user
    session = requests.Session()
    user = User.query.filter_by(username=username).first()
    assert user is not None, 'User does not exisst in database!'

    # Login user
    login_url = f'{url}/auth/login'
    response_login = session.post(login_url, json=login_data_username)
    assert response_login.status_code == 200, f"Login fehlgeschlagen! Status: {response_login.status_code}, Antwort: {response_login.text}"

    # Return test session
    yield session

    # Logout user
    logout_url = f'{url}/auth/logout'
    response_logout = session.post(logout_url)
    assert response_logout.status_code == 200, f'Error: Logout failed! Status: {response_logout.status_code}, Text: {response_logout.text}'

