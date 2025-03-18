import pytest
import requests

from app import app, db
from models import User, Destination, Activity
from werkzeug.security import generate_password_hash

from .helping_functions import get_dummy_data
from .helping_variables import url

@pytest.fixture(scope="module")
def setup_application():
    """Fixture zur Vorbereitung der Testdatenbank und Session."""
    # Setze den Application Context
    with app.app_context():
        # Leere die Datenbank
        db.drop_all()
        db.create_all()

        # Füge Dummy-Daten hinzu
        dummy_data = get_dummy_data()

        hashed_password = generate_password_hash(dummy_data['user']['password'])

        # Erstelle den Benutzer
        user = User(
            username=dummy_data['user']['username'],
            email=dummy_data['user']['email'],
            password=hashed_password,
            city=dummy_data['user']['city'],
            longitude=dummy_data['user']['longitude'],
            latitude=dummy_data['user']['latitude'],
            country=dummy_data['user']['country'],
            currency=dummy_data['user']['currency']
        )
        db.session.add(user)
        db.session.commit()

        # Erstelle die Destinations und Activities und verknüpfe sie mit dem User
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

        # Session für Tests vorbereiten
        session = requests.Session()
        login_url = f'{url}/login'
        login_data = {
            "identifier": "test_user",  # Benutzername
            "password": "testpassword123!"  # Passwort
        }
        #login_url = f'{url}/login'
        response_login = session.post(login_url, json=login_data)
        assert response_login.status_code == 200, f"Login fehlgeschlagen! Status: {response_login.status_code}, Antwort: {response_login.text}"

        yield session  # Session für Tests bereitstellen und Datenbankzugriff

        # Logout
        logout_url = f'{url}/logout'
        response_logout = session.post(logout_url)
        assert response_logout.status_code == 200, f"Fehler beim Logout! Statuscode: {response_logout.status_code}, Antwort: {response_logout.text}"

        # Bereinigen der db
        db.session.remove()
        db.drop_all()

