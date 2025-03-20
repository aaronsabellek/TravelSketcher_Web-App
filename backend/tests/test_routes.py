import requests
from models import User, Destination, Activity
from app import mail
from unittest.mock import patch

from helpers import generate_verification_token, send_verification_email

from .helping_variables import (
    url,
    dummy_data,
    registration_data,
    login_data_username,
    login_data_email,
    updated_profile_data,
    destination_data,
    activity_data,
)

from .helping_functions import (
    login,
    logout,
    get_profile_data,
    add_item,
    get_and_check_response,
    get_resource,
    edit_item,
    reorder_items
)


# FUNKTIONEN ZUM TESTEN DER ROUTES
'''
# Funktion zum Testen der Registration
def test_registration(setup_database):
    print("Test: Benutzerregistrierung")

    register_url = f"{url}/register"
    user_data=registration_data

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
'''
# Funktion zum Testen des Logins
def test_login(setup_database):
    print("Test: Login mit Username und mit Email")
    session = requests.Session()

    print("Login mit Benutzernamen")
    login(session, login_data_username)
    logout(session)

    print("Login mit Email")
    login(session, login_data_email)
    logout(session)

def test_verification_email(setup_database):
    # Annahme: Du hast einen User, der ein Verifikations-TOKEN benötigt
    user = User.query.filter_by(email=dummy_data['user']['email']).first()
    user.is_email_verified = False

    token = generate_verification_token(user.email)
    verify_url = f'{url}/verify_email/{token}'

    # Sendet eine GET-Anfrage an die Verifikationsroute
    response = setup_database.get(verify_url)
    assert response.status_code == 200
    assert b"E-Mail confirmed successfully!" in response.data

@patch('app.mail.send')
def test_send_verification_email(mock_send, setup_database):
    user = User.query.filter_by(email=dummy_data['user']['email']).first()
    user.is_email_verified = False

    send_verification_email(user)

    # Überprüfe, ob mail.send aufgerufen wurde
    mock_send.assert_called_once()
    msg = mock_send.call_args[0][0]  # Zugriff auf das erste Argument der Funktion
    assert msg.subject == "Please confirm your E-Mail"
    assert msg.recipients == [user.email]

# Funktion zum Testen der Anzeige der Profildaten
def test_get_profile(setup_logged_in_user):
    print("Test der Anzeige der Profildaten")

    profile_data = get_profile_data(setup_logged_in_user)
    assert profile_data is not None, "Fehler: Profil-Daten konnten nicht abgerufen werden!"

    print("Profil erfolgreich abgerufen!")

    for key, value in profile_data.items():
        print(f'{key}: {value}')

def test_edit_profile(setup_logged_in_user):
    print("Test des Bearbeitens des Profils")
    print(f"Versuch, Email zu ändern in: {updated_profile_data['email']}")
    edit_url = f'{url}/edit_profile'

    edit_item(setup_logged_in_user, edit_url, updated_profile_data, 'user')

def test_delete_profile(setup_database):
    """Testet das Löschen des Benutzerprofils."""
    session = session = requests.Session()
    login(session)

    delete_url = f'{url}/delete_profile'
    delete_response = session.delete(delete_url)
    print(f"Delete Response: {delete_response.status_code} - {delete_response.text}")
    assert delete_response.status_code == 200, "Profil konnte nicht gelöscht werden!"
    assert delete_response.json()['message'] == 'User deleted successfully'

    user_check = User.query.filter_by(username=dummy_data['user']['username']).first()
    assert user_check is None, "Benutzer wurde nicht aus der DB gelöscht!"

    profile_response = session.get(f'{url}/profile')
    assert profile_response.status_code in [401, 405], "Benutzer ist noch eingeloggt!" #401=Zugriff verweigert. 405=Weiterleitung an Login (post) mit get-Anfrage

#Funktion zum Testen des Hinzufügens einer Destination
def test_add_destination(setup_logged_in_user):
    print("Test zum Hinzufügen einer Destination")

    dest_url = f'{url}/add_destination'
    dest_data = destination_data

    expected_fields = [
            ('title', dest_data['title']),
            ('country', dest_data['country']),
            ('img_link', dest_data['img_link']),
            ('duration', dest_data['duration']),
            ('tags', dest_data['tags']),
            ('status', dest_data['status']),
            ('time', dest_data['time']),
            ('accomodation_link', dest_data['accomodation_link']),
            ('pricing', dest_data['pricing']),
            ('trip_pricing_flight', dest_data['trip_pricing_flight']),
            ('trip_pricing_no_flight', dest_data['trip_pricing_no_flight']),
            ('travel_duration_flight', dest_data['travel_duration_flight']),
            ('travel_duration_no_flight', dest_data['travel_duration_no_flight']),
            ('longitude', dest_data['longitude']),
            ('latitude', dest_data['latitude']),
            ('description', dest_data['description']),
            ('free_text', dest_data['free_text']),
        ]

    # Aufruf der Hilfsfunktion
    add_item(setup_logged_in_user, dest_url, dest_data, 'destination', expected_fields)

def test_get_destinations(setup_logged_in_user):
    print("Test zum Abrufen der Destinationen")

    # Teste nun die Route /get_destinations
    destinations_url = f'{url}/get_destinations'
    get_and_check_response(setup_logged_in_user, destinations_url, 'destination')

def test_get_destination(setup_logged_in_user):
    print("Test zum Abrufen einer spezifischen Destination")

    destination_id = 1
    get_resource(setup_logged_in_user, 'destination', destination_id)

# Funktion zum Testen des Bearbeitens einer Destination
def test_edit_destination(setup_logged_in_user):
    print("Test: Bearbeiten einer Destination")

    destination_id = 1  # ID der Destination, die bearbeitet werden soll

    edit_url = f'{url}/edit_destination/{destination_id}'

    edit_item(setup_logged_in_user, edit_url, destination_data, 'destination')

def test_reorder_destinations(setup_logged_in_user):
    print("Test zum Umsortieren von zwei Destinationen")

    destinations_url = f'{url}/get_destinations'
    reorder_url = f'{url}/reorder_destinations'

    # Nutzung der Hilfsfunktion
    reorder_items(setup_logged_in_user, destinations_url, reorder_url, "destinations")

def test_delete_destination(setup_logged_in_user):
    # Test, ob eine Destination mit der ID 1 gelöscht werden kann

    # Zuerst sicherstellen, dass die Destination existiert
    destination_id = 1
    delete_dest_url = f'{url}/delete_destination/{destination_id}'

    # API-Aufruf zum Löschen der Destination (DELETE-Request)
    response = setup_logged_in_user.delete(delete_dest_url, json=destination_id)
    print(f"Delete Response: {response.status_code} - {response.text}")
    assert response.status_code == 200

    # Überprüfen, dass die Nachricht "Destination deleted successfully" zurückgegeben wurde
    json_data = response.json()
    assert json_data['message'] == 'Destination deleted successfully'

    # Sicherstellen, dass die Destination nun aus der Datenbank gelöscht ist
    deleted_destination = Destination.query.filter_by(id=destination_id).first()
    assert deleted_destination is None

def test_add_activity(setup_logged_in_user):
    print("Test zum Hinzufügen einer Aktivität zu einer Destination")

    add_activity_url = f'{url}/add_activity'
    act_data = activity_data

    expected_fields = [
            ('title', act_data['title']),
            ('country', act_data['country']),
            ('duration', act_data['duration']),
            ('pricing', act_data['pricing']),
            ('status', act_data['status']),
            ('web_link', act_data['web_link']),
            ('img_link', act_data['img_link']),
            ('tags', act_data['tags']),
            ('trip_duration', act_data['trip_duration']),
            ('trip_pricing', act_data['trip_pricing']),
            ('longitude', act_data['longitude']),
            ('latitude', act_data['latitude']),
            ('description', act_data['description']),
            ('free_text', act_data['free_text']),
            ('destination_id', act_data['destination_id']),
        ]

    add_item(setup_logged_in_user, add_activity_url, activity_data, 'activity', expected_fields)

def test_get_activities(setup_logged_in_user):
    print('Test: Anzeigen der Activities einer Destination')

    destination_id = 1
    activities_url = f"{url}/get_activities/{destination_id}"
    get_and_check_response(setup_logged_in_user, activities_url, "activities")

def test_get_activity(setup_logged_in_user):
    print('Test: Anzeigen einer bestimmten Activity')

    activity_id = 1
    get_resource(setup_logged_in_user, 'activity', activity_id)

def test_edit_activity(setup_logged_in_user):
    print("Test: Bearbeiten einer Activity")

    activity_id = 2  # ID der Activity, die bearbeitet werden soll

    edit_url = f'{url}/edit_activity/{activity_id}'

    edit_item(setup_logged_in_user, edit_url, activity_data, 'activity')

def test_reorder_activities(setup_logged_in_user):
    print("Test zum Umsortieren von Activitie 2 und 3 der Destination 1")

    activities_url = f'{url}/get_activities'
    reorder_url = f'{url}/reorder_activities'

    # Nutzung der Hilfsfunktion
    destination_id = 1
    reorder_items(setup_logged_in_user, activities_url, reorder_url, "activities", destination_id=destination_id)

def test_delete_activity(setup_logged_in_user):
    # Teste das Löschen einer Activity (Erfolg)
    activity_id = 1
    delete_act_url = f'{url}/delete_activity/{activity_id}'

    response = setup_logged_in_user.delete(delete_act_url, json=activity_id)
    assert response.status_code == 200
    assert response.json()['message'] == 'Activity deleted successfully'

    # Teste, ob die Activity wirklich aus der Datenbank entfernt wurde
    deleted_activity = Activity.query.filter_by(id=activity_id).first()
    assert deleted_activity is None

def test_search(setup_logged_in_user):
    print("Test: Suche nach Schlagwort in Destinations und Activities")

    search_query = "frank"
    resource_type = "both"

    # URL der Such-API
    search_url = f'{url}/search'

    # Test mit 'search_query' und 'resource_type' als Parameter
    response = setup_logged_in_user.get(search_url, params={
        'search_query': search_query,
        'resource_type': resource_type
    })

    print(f'Search for "{search_query}" in resource type: {resource_type}')

    # Überprüfen, ob die Antwort den Statuscode 200 hat
    assert response.status_code == 200, f"Fehler bei der Suche. Statuscode: {response.status_code}, Antwort: {response.text}"

    # Ergebnisse aus der Antwort extrahieren
    data = response.json()
    assert 'results' in data, "Es wurden keine Ergebnisse gefunden."
    results = data['results']

    # Überprüfen, ob Ergebnisse zurückgegeben wurden
    assert len(results) > 0, f"Keine Ergebnisse für die Suche nach '{search_query}'"

    destinations = []
    activities = []

    for entry in results:
        if 'destination_id' in entry:  # Eintrag ist eine Activity (hat eine destination_id)
            activities.append(entry)
        else:  # Eintrag ist eine Destination
            destinations.append(entry)

    # Ausgabe der Destinations
    if destinations:
        print("Destinations:")
        for destination in destinations:
            print(f"Id: {destination['id']}, Title: {destination['title']}")

    # Ausgabe der Activities
    if activities:
        print("Activities:")
        for activity in activities:
            print(f"Id: {activity['id']}, Title: {activity['title']}")

    print("Suche erfolgreich durchgeführt und Ergebnisse überprüft!")

