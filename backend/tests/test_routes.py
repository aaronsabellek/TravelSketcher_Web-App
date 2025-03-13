import requests
from app import app
from models import User

from .test_helpers import (
    login_data_username,
    login_data_email,
    login, get_profile_data,
    edit_username, add_item,
    get_and_check_response,
    edit_item,
    url,
    reorder_items,
    logout
)

# FUNKTIONEN ZUM TESTEN DER ROUTES

# Funktion zum Testen der Registration
def test_registration():
    print("Test: Benutzerregistrierung")

    register_url = f"{url}/register"
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123!"
    }

    response = requests.post(register_url, json=user_data)
    assert response.status_code == 201, f"Fehler: Registrierung fehlgeschlagen! Status: {response.status_code}, Antwort: {response.text}"

    print("Benutzer erfolgreich registriert!")
    # Datenbankprüfung innerhalb des Kontextes
    with app.app_context():
        user = User.query.filter(
            (User.username == user_data['username']) | (User.email == user_data['email'])
        ).first()
    assert user is not None, f"Fehler: Benutzer wurde nicht korrekt in der Datenbank gespeichert! Gesucht: {user_data}"
    print(f"Benutzer erfolgreich in der Datenbank gefunden: {user.username}")

# Funktion zum Testen des Logins
def test_login():
    print("Test: Login mit Username und mit Email")
    #Beim Abrufen dieser Funktion Login und Logour herauskommentieren
    session = requests.Session()

    print("Login mit Benutzernamen")
    login(session, login_data_username)
    logout(session)

    print("Login mit Email")
    login(session, login_data_email)
    logout(session)

# Funktion zum Testen der Anzeige der Profildaten
def test_get_profile(session):
    print("Test der Anzeige der Profildaten")

    profile_data = get_profile_data(session)
    assert profile_data is not None, "Fehler: Profil-Daten konnten nicht abgerufen werden!"

    print("Profil erfolgreich abgerufen!")
    print(f"- Username: {profile_data['username']}")
    print(f"- E-Mail: {profile_data['email']}")
    print(f"- Bild-Link: {profile_data['img_link']}")

#Funktion zum Bearbeiten des Usernames
def test_edit_username(session):
    print("Test des Bearbeitens des Usernames")

    # Neuer Benutzername für den Test
    new_username = "testuser_edited"
    print(f"Versuch, den Username zu ändern in: {new_username}")
    edit_username(session, new_username)

    print("Username zurücksetzen")
    new_username = "testuser"
    edit_username(session, new_username)

#Funktion zum Testen des Hinzufügens einer Destination
def test_add_destination(session):
    print("Test zum Hinzufügen einer Destination")

    dest_url = f'{url}/add_destination'

    # Beispiel-Daten für die Destination
    dest_data = {
        'title': 'Bali',
        'country': 'Indonesia',
        'img_link': 'https://example.com/bali.jpg',
        'duration': '2 weeks',
        'tags': 'beach, adventure, culture',
        'status': 'planned',
        'months': 'May, June, July',
        'accomodation_link': 'https://example.com/bali-hotel',
        'accomodation_price': '800',
        'accomodation_text': 'Luxury resort near the beach',
        'trip_duration': '14 days',
        'trip_price': '1500',
        'trip_text': 'Includes flights and tours',
        'free_text': 'Must try the local cuisine and visit hidden waterfalls!'
    }

    expected_fields = [
            ('title', dest_data['title']),
            ('country', dest_data['country']),
            ('img_link', dest_data['img_link']),
            ('duration', dest_data['duration']),
            ('tags', dest_data['tags']),
            ('status', dest_data['status']),
            ('months', dest_data['months']),
            ('accomodation_link', dest_data['accomodation_link']),
            ('accomodation_price', dest_data['accomodation_price']),
            ('accomodation_text', dest_data['accomodation_text']),
            ('trip_duration', dest_data['trip_duration']),
            ('trip_price', dest_data['trip_price']),
            ('trip_text', dest_data['trip_text']),
            ('free_text', dest_data['free_text']),
        ]

    # Aufruf der Hilfsfunktion
    add_item(session, dest_url, dest_data, 'destination', expected_fields)

def test_get_destinations(session):
    print("Test zum Abrufen der Destinationen")

    # Teste nun die Route /get_destinations
    destinations_url = f'{url}/get_destinations'
    get_and_check_response(session, destinations_url, 'destination')

# Funktion zum Testen des Bearbeitens einer Destination
def test_edit_destination(session):
    print("Test: Bearbeiten einer Destination")

    destination_id = 1  # ID der Destination, die bearbeitet werden soll

    edit_url = f'{url}/edit_destination/{destination_id}'

    # Neue Werte für die Destination
    updated_data = {
        'title': 'Updated Destination Title',
        'country': 'Italien',
        'img_link': 'https://example.com/new_image.jpg',
        'duration': '7 Tage',
        'tags': 'Strand, Sommer, Erholung',
        'status': 'aktiv',
        'months': 'Juni, Juli, August',
        'accomodation_link': 'https://example.com/accomodation',
        'accomodation_price': '1500',
        'accomodation_text': 'Luxushotel am Meer',
        'trip_duration': '10 Tage',
        'trip_price': '2500',
        'trip_text': 'Erholung pur an der Amalfiküste',
        'free_text': 'Jetzt buchen und sparen!'
    }

    edit_item(session, edit_url, updated_data, 'destination')

def test_reorder_destinations(session):
    print("Test zum Umsortieren von zwei Destinationen")

    destinations_url = f'{url}/get_destinations'
    reorder_url = f'{url}/reorder_destinations'

    # Nutzung der Hilfsfunktion
    reorder_items(session, destinations_url, reorder_url, "destinations")


def test_add_activity(session):
    print("Test zum Hinzufügen einer Aktivität zu einer Destination")

    # Aktivitätsdaten
    activity_data = {
        'title': 'Wanderung im Gebirge',
        'country': 'Deutschland',
        'duration': '5 Stunden',
        'price': '20',
        'activity_text': 'Eine wunderschöne Wanderung mit atemberaubender Aussicht.',
        'status': 'aktiv',
        'web_link': 'http://example.com',
        'img_link': 'http://example.com/image.jpg',
        'tags': 'Wandern, Berge, Natur',
        'trip_duration': '7 Tage',
        'trip_price': '500',
        'trip_text': 'Entdecke die Berge in 7 Tagen',
        'free_text': 'Die Wanderung kann individuell angepasst werden.',
        'destination_id': 1
    }

    expected_fields = [
            ('title', activity_data['title']),
            ('country', activity_data['country']),
            ('duration', activity_data['duration']),
            ('price', activity_data['price']),
            ('activity_text', activity_data['activity_text']),
            ('status', activity_data['status']),
            ('web_link', activity_data['web_link']),
            ('img_link', activity_data['img_link']),
            ('tags', activity_data['tags']),
            ('trip_duration', activity_data['trip_duration']),
            ('trip_price', activity_data['trip_price']),
            ('trip_text', activity_data['trip_text']),
            ('free_text', activity_data['free_text']),
            ('destination_id', activity_data['destination_id']),
        ]

    # Anfrage zum Hinzufügen der Aktivität
    add_activity_url = f'{url}/add_activity'
    add_item(session, add_activity_url, activity_data, 'activity', expected_fields)

def test_get_activities(session):
    print('Test: Anzeigen der Activities einer Destination')

    destination_id = 1
    url = f"{url}/get_activities/{destination_id}"
    get_and_check_response(session, url, "activities")

def test_edit_activity(session):
    print("Test: Bearbeiten einer Activity")

    destination_id = 1  # ID der Destination, zu der die Activity gehört
    activity_id = 1  # ID der Activity, die bearbeitet werden soll

    edit_url = f'{url}/edit_activity/{destination_id}/{activity_id}'

    # Neue Werte für die Activity
    updated_data = {
        'title': 'Neue Aktivität',
        'country': 'Deutschland',
        'duration': '5',
        'price': '150.0',
        'activity_text': 'Dies ist die Beschreibung der neuen Aktivität.',
        'status': 'Aktiv',
        'web_link': 'https://example.com',
        'img_link': 'https://example.com/image.jpg',
        'tags': 'Abenteuer Natur',
        'trip_duration': '7',
        'trip_price': '500.0',
        'trip_text': 'Detaillierte Beschreibung der Reise',
        'free_text': 'Zusätzliche Informationen zur Reise'
    }

    edit_item(session, edit_url, updated_data, 'activity')

def test_reorder_activities(session):
    print("Test zum Umsortieren von Activitie 2 und 3 der Destination 1")

    activities_url = f'{url}/get_activities'
    reorder_url = f'{url}/reorder_activities'

    # Nutzung der Hilfsfunktion
    destination_id = 1
    reorder_items(session, activities_url, reorder_url, "activities", destination_id=destination_id)


# Ausführen der Tests
if __name__ == '__main__':
    # Comment out functions as needed

    #test_registration()
    #test_login()

    session = requests.Session()
    login(session)

    #test_get_profile(session)
    #test_edit_username(session)
    #test_add_destination(session)
    test_get_destinations(session)
    #test_edit_destination(session)
    #test_reorder_destinations(session)
    #test_add_activity(session)
    #test_get_activities(session)
    #test_edit_activity(session)
    #test_reorder_activities(session)

    logout(session)