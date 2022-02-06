from src import app

from tests.tokens import set_token

client = app.test_client()
url = '/editgame/8c19cafb-1eac-45e2-b089-c6e79b2e6c5e'

def test_get_editgame_route():
    """
    Testing editgame page with no session
    Method : GET
    """
    response = client.get(url)
    assert response.status_code == 302

def test_get_editgame_route_auth_user_per():
    """
    Testing page with user session
    Method : GET
    """
    set_token(client, "usertest")

    response = client.get(url)
    assert response.status_code == 302

def test_get_editgame_route_auth_admin_per():
    """
    Testing page with admin session
    Method : GET
    """
    set_token(client, "admin")

    response = client.get(url)
    assert response.status_code == 200