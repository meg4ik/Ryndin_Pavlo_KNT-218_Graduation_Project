from src import app

from tests.tokens import set_token

client = app.test_client()
url = '/user/f4685c53-5b46-4106-abfb-9d76c1fcb4cd'

def test_get_user_route():
    """
    Testing user page with no session
    Method : GET
    """
    response = client.get(url)
    assert response.status_code == 302

def test_get_user_route_wrong_user():
    """
    Testing user page with wrong user
    Method : GET
    """
    url = '/user/wrongc53-5b46-4106-abfb-9d76c1fcb4cd'
    set_token(client, "usertest")
    response = client.get(url)
    assert response.status_code == 302

def test_get_user_route_with_session():
    """
    Testing user page with session
    Method : GET
    """
    set_token(client, "usertest")
    response = client.get(url)
    assert response.status_code == 200