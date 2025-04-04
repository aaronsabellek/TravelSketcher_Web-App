import requests
import pytest

from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import User, Destination, Activity
from tests.dummy_data import dummy_data
from .helping_variables import (
    url,
    user,
    username,
    second_user,
    login_data_username,
    username
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

        # Set hashed password
        hashed_password = generate_password_hash(user['password'], method='pbkdf2:sha256')

         # Create main user in database
        main_user = User(
            id=user['id'],
            username=user['username'],
            email=user['email'],
            password=hashed_password,
            city=user['city'],
            longitude=user['longitude'],
            latitude=user['latitude'],
            country=user['country'],
            currency=user['currency'],
            is_email_verified=user['is_email_verified']
        )
        db.session.add(main_user)
        db.session.commit()

        # Create second user in database
        secondary_user = User(
            id=second_user['id'],
            username=second_user['username'],
            email=second_user['email'],
            password=hashed_password,
            city=second_user['city'],
            longitude=second_user['longitude'],
            latitude=second_user['latitude'],
            country=second_user['country'],
            currency=second_user['currency'],
            is_email_verified=second_user['is_email_verified']
        )
        db.session.add(secondary_user)
        db.session.commit()

        # Create destinations and activities of main user in database
        for dest_data in dummy_data['destinations']:
            destination = Destination(
                id=dest_data['id'],
                title=dest_data['title'],
                country=dest_data['country'],
                position=dest_data['position'],
                user_id=main_user.id
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

        # Create destinations and activities of second user in database
        for sec_dest_data in dummy_data['second_destinations']:
            second_destination = Destination(
                id=sec_dest_data['id'],
                title=sec_dest_data['title'],
                country=sec_dest_data['country'],
                position=sec_dest_data['position'],
                user_id=secondary_user.id
            )
            db.session.add(second_destination)
            db.session.commit()

            for sec_act_data in sec_dest_data['activities']:
                second_activity = Activity(
                    id=sec_act_data['id'],
                    title=sec_act_data['title'],
                    country=sec_act_data['country'],
                    position=sec_act_data['position'],
                    destination_id=second_destination.id
                )
                db.session.add(second_activity)

            db.session.commit()

        # Return test client
        with app.test_client() as client:
            yield client

        # Remove all data from database
        db.session.remove()
        db.drop_all()



@pytest.fixture(scope='function')
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
    assert 'user_id' not in session.cookies, 'User session is still active after logout!'

