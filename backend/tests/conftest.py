import pytest
import requests
from .helping_variables import url, login_data_username

@pytest.fixture(scope="session")
def session():
    """
    Erstellt eine Requests-Session, loggt sich ein und sorgt für einen sauberen Logout nach den Tests.
    """
    session = requests.Session()

    login_url = f'{url}/login'
    login_data = login_data_username

    response_login = session.post(login_url, json=login_data)
    assert response_login.status_code == 200, f"Login fehlgeschlagen! Status: {response_login.status_code}, Antwort: {response_login.text}"

    yield session  # Session für Tests bereitstellen

    # Logout
    logout_url = f'{url}/logout'
    response_logout = session.post(logout_url)

    assert response_logout.status_code == 200, f"Fehler beim Logout! Statuscode: {response_logout.status_code}, Antwort: {response_logout.text}"