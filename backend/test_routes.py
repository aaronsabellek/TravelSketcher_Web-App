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

def dashboard(session):
    dashboard_url = "http://127.0.0.1:5000/dashboard"

    response = session.get(dashboard_url)
    assert response.status_code == 200, f"Fehler beim Abrufen des Dashboards: {response.status_code} - {response.text}"

    data = response.json()
    destinations = data.get('destinations', [])
    print(f"Dashboard-Daten erfolgreich geladen! {len(destinations)} Destinationen gefunden.")
    return destinations

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

    response = session.post(edit_username_url, data=edit_data)
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
    response = session.post(url, data=data)
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
    assert isinstance(data, list) and len(data) > 0, f"Die {expected_key} sind leer oder keine Liste. Antwort: {data}"

    print(f"Gefundene {expected_key.capitalize()}:")
    for item in data:
        assert 'title' in item and 'id' in item, f"Fehler: 'title' oder 'id' fehlt im Element: {item}"
        print(f"- {item['title']} (ID: {item['id']})")

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
    session = requests.Session()

    print("Login mit Benutzernamen")
    login(session, login_data_username)
    dashboard(session)
    logout(session)

    print("Login mit Email")
    login(session, login_data_email)
    dashboard(session)
    logout(session)

# Funktion zum Testen der Anzeige der Profildaten
def test_get_profile():
    print("Test der Anzeige der Profildaten")
    session = requests.Session()
    login(session)

    profile_data = get_profile_data(session)
    assert profile_data is not None, "Fehler: Profil-Daten konnten nicht abgerufen werden!"

    print("Profil erfolgreich abgerufen!")
    print(f"- Username: {profile_data['username']}")
    print(f"- E-Mail: {profile_data['email']}")
    print(f"- Bild-Link: {profile_data['img_link']}")

    logout(session)

#Funktion zum Bearbeiten des Usernames
def test_edit_username():
    print("Test des Bearbeitens des Usernames")
    session = requests.Session()
    login(session)

    # Neuer Benutzername für den Test
    new_username = "testuser_edited"
    print(f"Versuch, den Username zu ändern in: {new_username}")
    edit_username(session, new_username)

    print("Username zurücksetzen")
    new_username = "testuser"
    edit_username(session, new_username)

    logout(session)

#Funktion zum Testen des Hinzufügens einer Destination
def test_add_destination():
    print("Test zum Hinzufügen einer Destination")
    session = requests.Session()
    login(session)

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

    logout(session)

def test_get_destinations():
    print("Test zum Abrufen der Destinationen")
    session = requests.Session()
    login(session)

    # Teste nun die Route /get_destinations
    destinations_url = 'http://127.0.0.1:5000/get_destinations'
    get_and_check_response(session, destinations_url, 'destination')

    logout(session)

# Funktion zum Testen des Bearbeitens einer Destination
def test_edit_destination():
    print("Test: Bearbeiten einer Destination")
    session = requests.Session()
    login(session)

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

    # API-Request senden
    response = session.post(edit_url, json=updated_data)

    # Überprüfen, ob die Antwort den Statuscode 200 zurückgibt
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Überprüfen, ob die Rückgabe die erwarteten Daten enthält
    response_data = response.json()

    # Hier prüfen wir, ob die geänderten Felder korrekt sind
    for key, value in updated_data.items():
        assert response_data['destination'][key] == value, f"Expected {key} to be {value}, but got {response_data['destination'][key]}"

    print("Destination erfolgreich aktualisiert!")
    print("Neue Daten der Destination:")
    for key, value in response_data['destination'].items():
        print(f"{key}: {value}")

    logout(session)

def test_reorder_destinations():
    print("Test zum Umsortieren von zwei Destinationen")
    session = requests.Session()
    login(session)

    #stattadessen get_and_check_response()?
    destinations_url = 'http://127.0.0.1:5000/get_destinations'
    get_response = session.get(destinations_url)

    assert get_response.status_code == 200, f"Fehler beim Abrufen der Destinationen. Statuscode: {get_response.status_code}, Antwort: {get_response.text}"
    print("Zugriff auf /get_destinations erfolgreich!")

    destinations = get_response.json()
    assert destinations, "Keine Destinationen gefunden."
    print("Gefundene Destinationen:")
    for destination in destinations:
        print(f"- {destination['title']} (ID: {destination['id']}, Position: {destination['position']})")

    # Wir nehmen an, dass die Destinationen nach ihrer Position sortiert sind
    dest_by_position = sorted(destinations, key=lambda x: x['position'])
    print(f"Destinationen nach Position sortiert: {[d['id'] for d in dest_by_position]}")

    # Sicherstellen, dass mindestens 3 Destinationen vorhanden sind
    assert len(dest_by_position) >= 3, "Fehler: Weniger als 3 Destinationen vorhanden!"

    # Überprüfe die IDs der Destinationen an den Positionen 2 und 3
    pos_2_id = dest_by_position[1]['id']  # ID der 2. Destination
    pos_3_id = dest_by_position[2]['id']  # ID der 3. Destination
    print(f"ID der 2. Destination: {pos_2_id}, ID der 3. Destination: {pos_3_id}")

    # Tausche nur die Positionen (nicht die IDs) der 2. und 3. Destination
    pos_2 = next(d for d in destinations if d['id'] == pos_2_id)
    pos_3 = next(d for d in destinations if d['id'] == pos_3_id)

    print(f"Vor dem Tausch: Position 2 = {pos_2['position']}, Position 3 = {pos_3['position']}")

    # Tausche nur die Positionen
    temp_position = pos_2['position']
    pos_2['position'] = pos_3['position']
    pos_3['position'] = temp_position

    print(f"Nach dem Tausch: Position 2 = {pos_2['position']}, Position 3 = {pos_3['position']}")

    # Übermittle nun die neue Reihenfolge mit den IDs der Destinationen
    new_order = [d['id'] for d in sorted(destinations, key=lambda x: x['position'])]
    print(f"Neue Reihenfolge der Destinationen: {new_order}")
    reorder_url = 'http://127.0.0.1:5000/reorder_destinations'
    reorder_response = session.post(reorder_url, json={"destinations": new_order})

    assert reorder_response.status_code == 200, f"Fehler beim Umsortieren der Destinationen. Statuscode: {reorder_response.status_code}, Antwort: {reorder_response.text}"
    print("Destinations erfolgreich umsortiert!")

    get_response = session.get(destinations_url)

    assert get_response.status_code == 200, f"Fehler beim Abrufen der Destinationen nach dem Umsortieren. Statuscode: {get_response.status_code}, Antwort: {get_response.text}"
    print("Zugriff auf /get_destinations erfolgreich!")

    destinations = get_response.json()

    # Stelle sicher, dass die Positionen korrekt umgetauscht wurden
    destination_1 = next(d for d in destinations if d['id'] == pos_2_id)
    destination_2 = next(d for d in destinations if d['id'] == pos_3_id)

    print(f"Nach dem Umsortieren: {destination_1['title']} (Position: {destination_1['position']}), {destination_2['title']} (Position: {destination_2['position']})")

    destinations = get_response.json()
    assert destinations, "Keine Destinationen gefunden."
    print("Gefundene Destinationen:")
    for destination in destinations:
        print(f"- {destination['title']} (ID: {destination['id']}, Position: {destination['position']})")

    assert destination_1['position'] == pos_2['position'], f"Fehler: {destination_1['title']} sollte Position {pos_2['position']} haben, hat aber Position {destination_1['position']}!"
    assert destination_2['position'] == pos_3['position'], f"Fehler: {destination_2['title']} sollte Position {pos_3['position']} haben, hat aber Position {destination_2['position']}!"

    logout(session)

def test_add_activity():
    print("Test zum Hinzufügen einer Aktivität zu einer Destination")
    session = requests.Session()
    login(session)

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
    # Aufruf der Hilfsfunktion
    add_item(session, add_activity_url, activity_data, 'activity', expected_fields)

    # Logout durchführen
    logout(session)

def test_reorder_activities():
    print("Test zum Umsortieren der Aktivitäten für eine Destination")
    session = requests.Session()
    login(session)

    # Abrufen der Aktivitäten für eine bestimmte Destination
    destination_id = 1  # Beispiel Destination ID
    get_activities_url = f'http://127.0.0.1:5000/get_activities/{destination_id}'
    get_response = session.get(get_activities_url)

    if get_response.status_code == 200:
        print("Zugriff auf /get_activities erfolgreich!")
        data = get_response.json()

        activities = data.get('activities', [])
        if activities:
            print("Gefundene Aktivitäten:")
            for activity in activities:
                print(f"- {activity['title']} (ID: {activity['id']}, Position: {activity['position']})")
        else:
            print("Keine Aktivitäten gefunden.")
            logout(session)
            return
    else:
        print(f"Fehler beim Abrufen der Aktivitäten. Statuscode: {get_response.status_code}")
        print(get_response.text)
        logout(session)
        return

    # Wir nehmen an, dass die Aktivitäten nach ihrer Position sortiert sind
    activities_by_position = sorted(activities, key=lambda x: x['position'])
    print(f"Aktivitäten nach Position sortiert: {[a['id'] for a in activities_by_position]}")

    # Überprüfe die IDs der Aktivitäten an den Positionen 2 und 3
    pos_2_id = activities_by_position[1]['id']  # ID der 2. Aktivität
    pos_3_id = activities_by_position[2]['id']  # ID der 3. Aktivität
    print(f"ID der 2. Aktivität: {pos_2_id}, ID der 3. Aktivität: {pos_3_id}")

    # Tausche nur die Positionen der Aktivitäten
    pos_2 = next(a for a in activities if a['id'] == pos_2_id)
    pos_3 = next(a for a in activities if a['id'] == pos_3_id)

    print(f"Vor dem Tausch: Position 2 = {pos_2['position']}, Position 3 = {pos_3['position']}")

    # Tausche die Positionen
    temp_position = pos_2['position']
    pos_2['position'] = pos_3['position']
    pos_3['position'] = temp_position

    print(f"Nach dem Tausch: Position 2 = {pos_2['position']}, Position 3 = {pos_3['position']}")

    # Übermittle nun die neue Reihenfolge mit den IDs der Aktivitäten
    new_order = [a['id'] for a in sorted(activities, key=lambda x: x['position'])]
    reorder_url = 'http://127.0.0.1:5000/reorder_activities'
    reorder_response = session.post(reorder_url, data={
        'destination_id': destination_id,
        'activities[]': new_order
    })

    if reorder_response.status_code == 200:
        print("Aktivitäten erfolgreich umsortiert!")
    else:
        print(f"Fehler beim Umsortieren der Aktivitäten. Statuscode: {reorder_response.status_code}")
        print(reorder_response.text)

    # Abrufen der Aktivitäten nach dem Umordnen
    get_response = session.get(get_activities_url)

    if get_response.status_code == 200:
        print("Zugriff auf /get_activities erfolgreich!")
        data = get_response.json()

        # Stelle sicher, dass die Positionen korrekt umgetauscht wurden
        activity_1 = next(a for a in data['activities'] if a['id'] == pos_2_id)
        activity_2 = next(a for a in data['activities'] if a['id'] == pos_3_id)

        assert activity_1['position'] == pos_3['position'], f"Fehler: {activity_1['title']} sollte Position {pos_3['position']} haben, hat aber Position {activity_1['position']}!"
        assert activity_2['position'] == pos_2['position'], f"Fehler: {activity_2['title']} sollte Position {pos_2['position']} haben, hat aber Position {activity_2['position']}!"

        # Ausgabe der aktuellen Positionen
        print(f"Nach dem Umsortieren: {activity_1['title']} (Position: {activity_1['position']}), {activity_2['title']} (Position: {activity_2['position']})")
    else:
        print(f"Fehler beim Abrufen der Aktivitäten. Statuscode: {get_response.status_code}")
        print(get_response.text)

    logout(session)

# Ausführen der Tests
if __name__ == '__main__':
    # Comment out functions as needed
    #test_registration()
    #test_login()
    #test_get_profile()
    #test_edit_username()
    #test_add_destination()
    #test_get_destinations()
    #test_edit_destination()
    test_reorder_destinations()
    #test_add_activity()
    #test_get_activities()
    #test_reorder_activities()