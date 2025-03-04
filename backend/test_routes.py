import requests

def test_registration():
    url = "http://127.0.0.1:5000/register"

    data = {
        'username': 'testuser',
        'password': '',
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
    # URL der Login-Route
    url = 'http://127.0.0.1:5000/login'

    # Deine Test-Benutzerdaten
    login_data = {
        'username': 'testuser',
        'password': 'testpassword123!'
    }

    # Starte eine Sitzung, um Cookies zu speichern (für die Authentifizierung)
    session = requests.Session()

    # Sende eine POST-Anfrage an den Server mit den Login-Daten
    response = session.post(url, data=login_data)

    # Überprüfe, ob der Login erfolgreich war (Statuscode 200)
    if response.status_code == 200:
        print("Login erfolgreich!")
        dashboard_url = 'http://127.0.0.1:5000/dashboard'
        dashboard_response = session.get(dashboard_url)

        if dashboard_response.status_code == 200:
            print("Zugriff auf Dashboard erfolgreich!")
        else:
            print(f"Fehler beim Zugriff auf das Dashboard. Statuscode: {dashboard_response.status_code}")
    else:
        print(f"Login fehlgeschlagen. Statuscode: {response.status_code}")
        print(response.text)

# Funktion zum Testen der Erstellung einer Destination
def test_add_destination():

    session = requests.Session()

    login_url = 'http://127.0.0.1:5000/login'
    login_data = {
        'username': 'testuser',
        'password': 'testpassword123!'
    }
    login_response = session.post(login_url, data=login_data)

    if login_response.status_code == 200:
        print("Login erfolgreich!")
    else:
        print(f"Login fehlgeschlagen. Statuscode: {login_response.status_code}")
        print(login_response.text)
        return

    dest_url = 'http://127.0.0.1:5000/add_destination'

    # Beispiel-Daten für die Destination
    dest_data = {
        'title': 'New Destination'
    }


    add_response = session.post(dest_url, data=dest_data)
    print(f"Add Destination Status Code: {add_response.status_code}")

    # Prüfen, ob die Destination erfolgreich hinzugefügt wurde
    if add_response.status_code == 200:
        print("Destination added successfully!")
    else:
        print("Failed to add destination. Check response!")
        print(add_response.text)


def test_get_destinations():
    # Erstelle eine Session
    session = requests.Session()

    login_url = 'http://127.0.0.1:5000/login'
    login_data = {
        'username': 'testuser',
        'password': 'testpassword123!'
    }
    login_response = session.post(login_url, data=login_data)

    if login_response.status_code == 200:
        print("Login erfolgreich!")
    else:
        print(f"Login fehlgeschlagen. Statuscode: {login_response.status_code}")
        print(login_response.text)
        return

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

#Test reorder_destinations-route with position 2 and 3
def test_reorder_destinations():
    session = requests.Session()

    login_url = 'http://127.0.0.1:5000/login'
    login_data = {
        'username': 'testuser',
        'password': 'testpassword123!'
    }
    login_response = session.post(login_url, data=login_data)

    if login_response.status_code == 200:
        print("Login erfolgreich!")
    else:
        print(f"Login fehlgeschlagen. Statuscode: {login_response.status_code}")
        print(login_response.text)
        return

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
            return
    else:
        print(f"Fehler beim Abrufen der Destinationen. Statuscode: {get_response.status_code}")
        print(get_response.text)
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
            return
    else:
        print(f"Fehler beim Abrufen der Destinationen. Statuscode: {get_response.status_code}")
        print(get_response.text)
        return


if __name__ == '__main__':
    # Comment out functions as needed
    #test_registration()
    #test_login()
    #test_add_destination()
    #test_get_destinations()
    test_reorder_destinations()
