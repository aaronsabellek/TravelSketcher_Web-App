import requests

def test_registration():
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


if __name__ == '__main__':
    #print("Test-Login durchführen:")
    #test_add_destination()
    test_get_destinations()
