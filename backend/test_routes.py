import requests

login_data_username = {
    'identifier': 'testuser',
    'password': 'testpassword123!'
}

login_data_email = {
    'identifier': 'testuser@example.com',
    'password': 'testpassword123!'
}

# HILFSFUNKTIONEN

#Hilsfunktion zum Login
def login(session, login_data=None):
    login_url = 'http://127.0.0.1:5000/login'

    # Standard-Login-Daten setzen, wenn kein login_data übergeben wurde

    login_data = login_data or login_data_username

    response = session.post(login_url, data=login_data)

    if response.status_code == 200:
        print("Login erfolgreich.")
    else:
        print(f"Login fehlgeschlagen. Statuscode: {response.status_code}")
        print(response.text)

def dashboard(session):
    dashboard_url = 'http://127.0.0.1:5000/dashboard'
    dashboard_response = session.get(dashboard_url)
    if dashboard_response.status_code == 200:
        print("Zugriff auf Dashboard nach Login mit Benutzername erfolgreich!")
    else:
        print(f"Fehler beim Zugriff auf das Dashboard. Statuscode: {dashboard_response.status_code}")

def get_profile_data(session):
    profile_url = 'http://127.0.0.1:5000/profile'

    response = session.get(profile_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler beim Abrufen des Profils. Statuscode: {response.status_code}")
        print(response.text)
        return None

def show_username(session):
    profile_data = get_profile_data(session)
    if profile_data:
        print(f"Username: {profile_data['username']}")
    else:
        print("Konnte den Benutzernamen nicht abrufen.")

def edit_username(session, new_username):
    edit_username_url = 'http://127.0.0.1:5000/edit_username'
    edit_data = {'new_username': new_username}
    edit_response = session.post(edit_username_url, data=edit_data)

    if edit_response.status_code == 200:
        print("Benutzername erfolgreich geändert!")
        print("Neuer Benutzername:", edit_response.json().get('new_username'))
    else:
        print(f"Fehler beim Ändern des Benutzernamens! Statuscode: {edit_response.status_code}")
        print(edit_response.text)

    show_username(session)

#Hilfsfunktion zum Logout
def logout(session):
    logout_url = 'http://127.0.0.1:5000/logout'
    response = session.get(logout_url)

    if response.status_code == 200:
        print("Logout erfolgreich!")
    else:
        print("Fehler beim Logout!")


# FUNKTIONEN ZUM TESTEN DER ROUTES

# Funktion zum Testen der Registration
def test_registration():
    print("Test der Registration")

    url = "http://127.0.0.1:5000/register"

    data = {
        'username': 'testuser',
        'password': 'testpassword123!',
        'email': 'testuser@example.com'
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Registration successful!")
    else:
        print(f"Failed to register. Status Code: {response.status_code}")
        print("Response Text:", response.text)

# Funktion zum Testen des Logins
def test_login():
    print("Test des Logins mit Username und mit Email")
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
    if profile_data:
        print("Profil erfolgreich abgerufen!")
        print(f"- ID: {profile_data['id']}")
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
    print("Username ändern")
    new_username = "testuser_edited"
    edit_username(session, new_username)

    print("Username zurücksetzen")
    new_username = "testuser"
    edit_username(session, new_username)

    logout(session)

# Funktion zum Testen der Erstellung einer Destination
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

    add_response = session.post(dest_url, data=dest_data)
    print(f"Add Destination Status Code: {add_response.status_code}")

    # Prüfen, ob die Destination erfolgreich hinzugefügt wurde
    if add_response.status_code == 200:
        print("Destination added successfully!")
    else:
        print("Failed to add destination. Check response!")
        print(add_response.text)

    logout(session)

def test_get_destinations():
    print("Test zum Abrufen einer Destination")
    session = requests.Session()
    login(session)

    # Teste nun die Route /get_destinations
    destinations_url = 'http://127.0.0.1:5000/get_destinations'
    get_response = session.get(destinations_url)

    if get_response.status_code == 200:
        print("Zugriff auf /get_destinations erfolgreich!")
        destinations = get_response.json()
        if destinations:
            print("Gefundene Destinationen:")
            for destination in destinations:
                print(f"- {destination['title']} (ID: {destination['id']}, Position: {destination['position']})")
        else:
            print("Keine Destinationen gefunden.")
    else:
        print(f"Fehler beim Abrufen der Destinationen. Statuscode: {get_response.status_code}")
        print(get_response.text)

    logout(session)

#Test reorder_destinations-route with position 2 and 3
def test_reorder_destinations():
    print("Test zum Umsortieren von zwei Destinationen")
    session = requests.Session()
    login(session)

    destinations_url = 'http://127.0.0.1:5000/get_destinations'
    get_response = session.get(destinations_url)

    if get_response.status_code == 200:
        print("Zugriff auf /get_destinations erfolgreich!")
        destinations = get_response.json()
        if destinations:
            print("Gefundene Destinationen:")
            for destination in destinations:
                print(f"- {destination['title']} (ID: {destination['id']}, Position: {destination['position']})")
        else:
            print("Keine Destinationen gefunden.")
            logout(session)
            return
    else:
        print(f"Fehler beim Abrufen der Destinationen. Statuscode: {get_response.status_code}")
        print(get_response.text)
        logout(session)
        return

    # Wir nehmen an, dass die Destinationen nach ihrer Position sortiert sind
    dest_by_position = sorted(destinations, key=lambda x: x['position'])
    print(f"Destinationen nach Position sortiert: {[d['id'] for d in dest_by_position]}")

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
    reorder_url = 'http://127.0.0.1:5000/reorder_destinations'
    reorder_response = session.post(reorder_url, json={"destinations": new_order})

    if reorder_response.status_code == 200:
        print("Destinations erfolgreich umsortiert!")
    else:
        print(f"Fehler beim Umsortieren der Destinationen. Statuscode: {reorder_response.status_code}")
        print(reorder_response.text)

    get_response = session.get(destinations_url)

    if get_response.status_code == 200:
        print("Zugriff auf /get_destinations erfolgreich!")
        destinations = get_response.json()
        if destinations:
            print("Gefundene Destinationen:")
            for destination in destinations:
                print(f"- {destination['title']} (ID: {destination['id']}, Position: {destination['position']})")
        else:
            print("Keine Destinationen gefunden.")
    else:
        print(f"Fehler beim Abrufen der Destinationen. Statuscode: {get_response.status_code}")
        print(get_response.text)

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

    # Anfrage zum Hinzufügen der Aktivität
    add_activity_url = 'http://127.0.0.1:5000/add_activity'
    response = session.post(add_activity_url, data=activity_data)

    # Überprüfen, ob die Aktivität erfolgreich hinzugefügt wurde
    if response.status_code == 200:
        print("Aktivität erfolgreich hinzugefügt!")
        activity_data = response.json()
        print(f"ID der Aktivität: {activity_data['activity']['id']}")
        print(f"Title: {activity_data['activity']['title']}")
        print(f"Status: {activity_data['activity']['status']}")
        print(f"Destination ID: {activity_data['activity']['destination_id']}")
    else:
        print(f"Fehler beim Hinzufügen der Aktivität. Statuscode: {response.status_code}")
        print(response.text)

    # Logout durchführen
    logout(session)

def test_get_activities():
    print("Test zum Abrufen der Aktivitäten für eine Destination")
    session = requests.Session()
    login(session)

    # ID der Destination, für die Aktivitäten abgerufen werden sollen
    destination_id = 1  # Falls du eine spezifische ID testen willst, ggf. anpassen

    # Anfrage zum Abrufen der Aktivitäten
    get_activities_url = f'http://127.0.0.1:5000/get_activities/{destination_id}'
    response = session.get(get_activities_url)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        print("Aktivitäten erfolgreich abgerufen!")
        data = response.json()
        print(f"Destination: {data['destination']}")
        print("Gefundene Aktivitäten:")
        for activity in data['activities']:
            print(f"- ID: {activity['id']}, Title: {activity['title']}, Status: {activity['status']}")
    else:
        print(f"Fehler beim Abrufen der Aktivitäten. Statuscode: {response.status_code}")
        print(response.text)

    # Logout durchführen
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
    #test_reorder_destinations()
    #test_add_activity()
    test_get_activities()