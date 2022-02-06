from src import app
from tests.tokens import set_token

client = app.test_client()
url = '/game/8c19cafb-1eac-45e2-b089-c6e79b2e6c5e'

def test_get_game_route():
    """
    Testing game page with no session
    Method : GET
    """
    response = client.get(url)
    assert response.status_code == 200

def test_get_game_route_user_session():
    """
    Testing game page with user session
    Method : GET
    """

    set_token(client, "usertest")
    response = client.get(url)
    assert response.status_code == 202

def test_get_game_route_wrong_uuid():
    """
    Testing game page with wrong uuid
    Method : GET
    """
    url = '/game/wrongafb-1eac-45e2-b089-c6e79b2e6c5e'
    response = client.get(url)
    assert response.status_code == 302

def test_post_game_route_wrong_uuid():
    """
    Testing game page with wrong uuid
    Method :POST
    """
    url = '/game/wrongafb-1eac-45e2-b089-c6e79b2e6c5e'
    set_token(client, "usertest")
    response = client.get(url)
    assert response.status_code == 302