import requests
import time
import pytest

from app.routes.helpers import generate_token
from tests.helping_variables import (
    url,
    mailhog_v2,
    mailhog_v1,
    email,
    login_data_username,
    registration_base_data
)


# Clear MailHog mailbox
def clear_mailhog():
    requests.delete(mailhog_v1)

# Send request and validate output
def request_and_validate(client, endpoint, test_data, method='POST', json_method=None):

    # Set url
    response_url = f'{url}/{endpoint}'

    # Use route
    if method == 'GET':
        response = client.get(response_url)
    else:
        response = client.post(response_url, json=test_data)

    # Set response data
    if json_method == True:
        response_data = response.json()
    else:
        response_data = response.json

    # Check for expected status
    assert response.status_code == test_data['expected_status'], f'Error: Unexpected status code! Status: {response.status_code}, Text: {response.text}'

    # Stop the test if thrown error message was expected
    if response.status_code not in [200, 201]:
        assert test_data['expected_message'] in response_data['error'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'
        return response

    # Check for expected message
    assert test_data['expected_message'] in response_data['message'], f'Error: Unexpected message. Status: {response.status_code}, Text: {response.text}'

    return response

# Check for incoming Mail by subject
def check_for_mail(subject):

    time.sleep(1) # Wait one second for MailHog to receive the validation mail

    # Send request to MailHog
    response = requests.get(mailhog_v2)
    assert response.status_code == 200, f'Error: No Connection to MailHog! Status: {response.status_code}, Text: {response.text}'

    # Check if latest email fits the validation mail
    latest_email = response.json()['items'][0]
    assert latest_email, f'Error: No E-Mail found in MailHog! Status: {response.status_code}, Text: {response.text}'
    assert latest_email['Content']['Headers']['Subject'][0] == subject, \
        f'Error: Subject of the latest Mail does not fit the validation mail!' \
        f'Status: {response.status_code}, Text: {response.text}'

    clear_mailhog() # Clear MailHog from all E-mails

    return response

def create_test_token(test_data, salt, email=email):

    # Generate token
    token = generate_token(email=email, salt=salt)

    # Set token as invalid if this should be tested
    for data in test_data:
        if 'invalid_token' in data:
            token = 'invalid_token'

    return token

# Login user
def login(client, login_data=login_data_username):

    login_url = f'{url}/auth/login'
    response = client.post(login_url, json=login_data)
    assert response.status_code == 200, f'Error: Login failed! Status: {response.status_code}, Text: {response.text}'

    return client

# Register user
def register(client):

    register_url = f'{url}/auth/register'
    response = client.post(register_url, json=registration_base_data)
    assert response.status_code in [200, 201], f'Error: Registration failed! Status: {response.status_code}, Text: {response.text}'

    return response





'''

#Login mit einem bestimmten Datenpaket
def login(session, login_data=None):
    login_url = f'{url}/login'
    login_data = login_data or login_data_username

    response = session.post(login_url, json=login_data)
    assert response.status_code == 200, f"Login fehlgeschlagen! Status: {response.status_code}, Antwort: {response.text}"

    print('Login erfolgreich!')

#Hilfsfunktion zum Logout
def logout(session):
    logout_url = f'{url}/logout'
    response = session.post(logout_url)

    assert response.status_code == 200, f"Fehler beim Logout! Statuscode: {response.status_code}, Antwort: {response.text}"
    print("Logout erfolgreich!")

#Holen von Profildaten
def get_profile_data(session):
    print("Test: Abruf der Profildaten")
    profile_url = f'{url}/profile'

    response = session.get(profile_url)
    assert response.status_code == 200, f"Fehler: Unerwarteter Statuscode {response.status_code}, Antwort: {response.text}"

    profile_data = response.json()
    print("Profildaten erfolgreich abgerufen!")

    return profile_data

#Item hinzufügen (Destination oder Activity)
def add_item(session, url, data, item_key, expected_fields):
# Anfrage zum Hinzufügen
    response = session.post(url, json=data)
    print(f"Add Item Status Code: {response.status_code}")
    assert response.status_code in [200, 201], f"Fehler beim Hinzufügen von {item_key}. Statuscode: {response.status_code}, Antwort: {response.text}"

    print(f"{item_key} erfolgreich hinzugefügt!")

    # Antwortdaten als JSON
    response_data = response.json()

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

def get_resource(session, resource_type, resource_id):
    """
    Hilfsfunktion, um eine Ressource abzurufen und zu testen.
    """
    get_url = f'{url}/get_{resource_type}/{resource_id}'

    response = session.get(get_url)
    assert response.status_code == 200, f"Fehler beim Abrufen von {resource_type} {resource_id}. Statuscode: {response.status_code}, Antwort: {response.text}"
    print(f"Zugriff auf {resource_type.capitalize()} {resource_id} erfolgreich!")

    data = response.json()

    for key, value in data.items():
        print(f'{key}: {value}')

def edit_item(session, edit_url, updated_data, item_key):
    # API-Request senden
    response = session.post(edit_url, json=updated_data)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Überprüfen, ob die Rückgabe die erwarteten Daten enthält
    response_data = response.json()

    for key, value in updated_data.items():
        if isinstance(value, list):
            # Wenn der Wert eine Liste ist (z. B. für "tags"), vergleichen wir die Listen
            assert sorted(response_data[item_key][key]) == sorted(value), f"Expected {key} to be {value}, but got {response_data[item_key][key]}"
        else:
            assert response_data[item_key][key] == value, f"Expected {key} to be {value}, but got {response_data[item_key][key]}"

    print(f"{item_key.capitalize()} erfolgreich aktualisiert!")
    print(f"Neue Daten der {item_key.capitalize()}:")
    for key, value in response_data[item_key].items():
        if key != 'password':
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
'''
