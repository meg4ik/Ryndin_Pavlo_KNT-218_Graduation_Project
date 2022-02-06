from src import app

from tests.tokens import set_token

client = app.test_client()
url = '/'

def test_get_main_route():
    """
    Testing main page with no session
    Method : GET
    """
    response = client.get(url)
    assert response.status_code == 200

def test_get_main_route_auth():
    """
    Testing main page with user session
    Method : GET
    """
    set_token(client, "usertest")

    response = client.get(url)
    assert response.status_code == 202