from src import app

from tests.tokens import set_token

client = app.test_client()
url = '/carts'

def test_get_carts_route():
    """
    Testing carts page with no session
    Method : GET
    """
    response = client.get(url)
    assert response.status_code == 200

def test_get_carts_route_with_session():
    """
    Testing carts page with user session
    Method : GET
    """
    set_token(client, "usertest")

    response = client.get(url)
    assert response.status_code == 202

def test_get_carts_route_with_wrong_role():
    """
    Testing carts page with user session
    Method : GET
    """
    set_token(client, "admin")

    response = client.get(url)
    assert response.status_code == 302

def test_post_carts_route():
    """
    Testing carts page
    Method : POST
    """

    response = client.post(url)
    assert response.status_code == 302