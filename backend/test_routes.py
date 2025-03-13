import requests
from app import app
from models import User

login_data_username = {
    'identifier': 'testuser',
    'password': 'testpassword123!'
}

login_data_email = {
    'identifier': 'testuser@example.com',
    'password': 'testpassword123!'
}

# HILFSFUNKTIONEN

#Login mit einem bestimmten Datenpaket
def login(session, login_data=None):
    login_url = 'http://127.0.0.1:5000/login'
    login_data = login_data or login_data_username

    response = session.post(login_url, json=login_data)
    assert response.status_code == 200, f"Login fehlgeschlagen! Status: {response.status_code}, Antwort: {response.text}"

    print('Login erfolgreich!')

#Holen von Profildaten
def get_profile_data(session):
    print("Test: Abruf der Profildaten")
    profile_url = 'http://127.0.0.1:5000/profile'

    response = session.get(profile_url)
    assert response.status_code == 200, f"Fehler: Unerwarteter Statuscode {response.status_code}, Antwort: {response.text}"

    profile_data = response.json()
    print("Profildaten erfolgreich abgerufen!")

    return profile_data

#Verändern des Usernames
def edit_username(session, new_username):
    edit_username_url = 'http://127.0.0.1:5000/edit_username'
    edit_data = {'new_username': new_username}

    response = session.post(edit_username_url, json=edit_data)
    assert response.status_code == 200, f"Fehler beim Ändern des Benutzernamens! Status: {response.status_code}, Antwort: {response.text}"

    print("Benutzername erfolgreich geändert")

    profile_data = get_profile_data(session)
    assert profile_data is not None, "Fehler: Profil-Daten konnten nicht abgerufen werden!"
    assert profile_data['username'] == new_username, (
        f"Fehler: Erwarteter Username '{new_username}', aber erhalten: '{profile_data['username']}'"
    )

    print(f"Benutzername erfolgreich geändert und überprüft: {profile_data['username']}")

#Item hinzufügen (Destination oder Activity)
def add_item(session, url, data, item_key, expected_fields):
# Anfrage zum Hinzufügen
    response = session.post(url, json=data)
    print(f"Add Item Status Code: {response.status_code}")
    assert response.status_code in [200, 201], f"Fehler beim Hinzufügen von {item_key}. Statuscode: {response.status_code}, Antwort: {response.text}"

    print(f"{item_key} erfolgreich hinzugefügt!")

    # Antwortdaten als JSON
    response_data = response.json()
    print("Response Data:", response_data)

    # Item aus der Antwort extrahieren
    item = response_data.get(item_key, {})

    # Sicherstellen, dass das Item existiert
    assert item, f"Fehler: Das hinzugefügte {item_key} wurde nicht in der Antwort gefunden."

    # Schleife über alle erwarteten Felder und prüfe die Übereinstimmung
    for field, expected_value in expected_fields:
        actual_value = item.get(field)
        assert actual_value == expected_value, (
            f"Fehler: {field} sollte '{expected_value}' sein, "
            f"aber ist '{actual_value}' in der Antwort."
        )

#Anfrage stellen
def get_and_check_response(session, url, expected_key):
    response = session.get(url)
    assert response.status_code == 200, f"Fehler beim Abrufen von {expected_key}. Statuscode: {response.status_code}, Antwort: {response.text}"
    print(f"Zugriff auf {url} erfolgreich!")

    # JSON-Daten extrahieren
    data = response.json()

    if isinstance(data, list):
        items = data  # Falls es eine Liste ist, direkt verwenden
    elif isinstance(data, dict) and expected_key in data:
        items = data[expected_key]  # Falls es ein Dict ist, die erwartete Liste extrahieren
    else:
        assert False, f"Unerwartetes Format der Antwort für {expected_key}. Antwort: {data}"

    assert data, f"Fehler: Die Antwort für {expected_key} ist leer oder ungültig. Antwort: {data}"

    print(f"Gefundene {expected_key.capitalize()}:")
    for item in items:
        assert 'title' in item and 'id' in item, f"Fehler: 'title' oder 'id' fehlt im Element: {item}"
        print(f"- {item['title']} (ID: {item['id']})")

def edit_item(session, edit_url, updated_data, item_key):
    print(f"Test: Bearbeiten einer {item_key.capitalize()}")

    # API-Request senden
    response = session.post(edit_url, json=updated_data)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Überprüfen, ob die Rückgabe die erwarteten Daten enthält
    response_data = response.json()

    # Hier prüfen wir, ob die geänderten Felder korrekt sind
    for key, value in updated_data.items():
        if isinstance(value, list):
            # Wenn der Wert eine Liste ist (z. B. für "tags"), vergleichen wir die Listen
            assert sorted(response_data[item_key][key]) == sorted(value), f"Expected {key} to be {value}, but got {response_data[item_key][key]}"
        else:
            assert response_data[item_key][key] == value, f"Expected {key} to be {value}, but got {response_data[item_key][key]}"

    print(f"{item_key.capitalize()} erfolgreich aktualisiert!")
    print(f"Neue Daten der {item_key.capitalize()}:")
    for key, value in response_data[item_key].items():
        print(f"{key}: {value}")

def reorder_items(session, url, reorder_url, item_key, destination_id=None):
    # 1. Abrufen der aktuellen Elemente
    if destination_id:
        get_url = f'{url}/{destination_id}'
        reorder_url = f'{reorder_url}/{destination_id}'
    else:
        get_url = url
        reorder_url = reorder_url

    get_response = session.get(get_url)
    assert get_response.status_code == 200, f"Fehler beim Abrufen der {item_key}. Statuscode: {get_response.status_code}, Antwort: {get_response.text}"
    print(f"Zugriff auf {url} erfolgreich!")

    items = get_response.json()

    if item_key == 'activities': items = items.get("activities", [])

    assert items, f"Keine {item_key} gefunden."
    print(f"Gefundene {item_key}:")
    for item in items:
        print(f"- {item['title']} (ID: {item['id']}, Position: {item['position']})")

    # 2. Sortieren nach Position
    sorted_items = sorted(items, key=lambda x: x['position'])
    assert len(sorted_items) >= 3, f"Fehler: Es gibt weniger als 2 {item_key} zum Tauschen!"

    # 3. IDs der zu tauschenden Items speichern
    item_1_id = sorted_items[1]['id']
    item_2_id = sorted_items[2]['id']
    print(f"Vor dem Tausch: ID {item_1_id} hat Position {sorted_items[1]['position']}, ID {item_2_id} hat Position {sorted_items[2]['position']}")

    # 4. Positionen tauschen
    sorted_items[1]['position'], sorted_items[2]['position'] = sorted_items[2]['position'], sorted_items[1]['position']

    # 5. Neue Reihenfolge vorbereiten
    new_order = [item['id'] for item in sorted(sorted_items, key=lambda x: x['position'])]

    # 6. API-Aufruf zum Neusortieren
    reorder_response = session.post(reorder_url, json={item_key: new_order, "destination_id": destination_id} if destination_id else {item_key: new_order})
    assert reorder_response.status_code == 200, f"Fehler beim Umsortieren der {item_key}. Statuscode: {reorder_response.status_code}, Antwort: {reorder_response.text}"
    print(f"{item_key.capitalize()} erfolgreich umsortiert!")

    # 7. Neue Reihenfolge abrufen und überprüfen
    get_response = session.get(get_url)
    assert get_response.status_code == 200, f"Fehler beim erneuten Abrufen der {item_key}. Statuscode: {get_response.status_code}, Antwort: {get_response.text}"

    items_after = get_response.json()

    if item_key == 'activities': items_after = items_after.get("activities", [])

    assert items_after, f"Keine {item_key} gefunden nach dem Umsortieren."

    # 8. Sicherstellen, dass die Positionen tatsächlich getauscht wurden
    item_1_after = next(a for a in items_after if a['id'] == item_1_id)
    item_2_after = next(a for a in items_after if a['id'] == item_2_id)

    print(f"Nach dem Umsortieren: ID {item_1_after['id']} hat Position {item_1_after['position']}, ID {item_2_after['id']} hat Position {item_2_after['position']}")

    assert item_1_after['position'] == sorted_items[1]['position'], f"Fehler: {item_key.capitalize()} {item_1_after['id']} sollte Position {sorted_items[1]['position']} haben, hat aber {item_1_after['position']}!"
    assert item_2_after['position'] == sorted_items[2]['position'], f"Fehler: {item_key.capitalize()} {item_2_after['id']} sollte Position {sorted_items[2]['position']} haben, hat aber {item_2_after['position']}!"

    print("Test erfolgreich abgeschlossen!")

#Hilfsfunktion zum Logout
def logout(session):
    logout_url = 'http://127.0.0.1:5000/logout'
    response = session.get(logout_url)

    assert response.status_code == 200, f"Fehler beim Logout! Statuscode: {response.status_code}, Antwort: {response.text}"
    print("Logout erfolgreich!")


# FUNKTIONEN ZUM TESTEN DER ROUTES

# Funktion zum Testen der Registration
def test_registration():
    print("Test: Benutzerregistrierung")

    register_url = "http://127.0.0.1:5000/register"
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

    dest_url = 'http://127.0.0.1:5000/add_destination'

    # Beispiel-Daten für die Destination
    dest_data = {
        'title': 'Bali Adventure',
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
    destinations_url = 'http://127.0.0.1:5000/get_destinations'
    get_and_check_response(session, destinations_url, 'destination')

# Funktion zum Testen des Bearbeitens einer Destination
def test_edit_destination(session):
    print("Test: Bearbeiten einer Destination")

    destination_id = 1  # ID der Destination, die bearbeitet werden soll

    edit_url = f'http://127.0.0.1:5000/edit_destination/{destination_id}'

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

    destinations_url = 'http://127.0.0.1:5000/get_destinations'
    reorder_url = 'http://127.0.0.1:5000/reorder_destinations'

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
    add_activity_url = 'http://127.0.0.1:5000/add_activity'
    add_item(session, add_activity_url, activity_data, 'activity', expected_fields)

def test_get_activities(session):
    print('Test: Anzeigen der Activities einer Destination')

    destination_id = 1
    url = f"http://127.0.0.1:5000/get_activities/{destination_id}"
    get_and_check_response(session, url, "activities")

def test_edit_activity(session):
    print("Test: Bearbeiten einer Activity")

    destination_id = 1  # ID der Destination, zu der die Activity gehört
    activity_id = 1  # ID der Activity, die bearbeitet werden soll

    edit_url = f'http://127.0.0.1:5000/edit_activity/{destination_id}/{activity_id}'

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

    activities_url = 'http://127.0.0.1:5000/get_activities'
    reorder_url = 'http://127.0.0.1:5000/reorder_activities'

    # Nutzung der Hilfsfunktion
    destination_id = 1
    reorder_items(session, activities_url, reorder_url, "activities", destination_id=destination_id)


# Ausführen der Tests
if __name__ == '__main__':
    # Comment out functions as needed

    session = requests.Session()
    login(session)

    #test_registration()
    #test_login()
    #test_get_profile(session)
    #test_edit_username(session)
    #test_add_destination(session)
    #test_get_destinations(session)
    #test_edit_destination(session)
    #test_reorder_destinations(session)
    #test_add_activity(session)
    test_get_activities(session)
    #test_edit_activity(session)
    #test_reorder_activities(session)

    logout(session)