from src import app

from tests.tokens import set_token

client = app.test_client()
url = '/buygame'

def test_post_buygame_route():
    """
    Testing buygame page with no session
    Method : POST
    """
    
    response = client.post(url)
    assert response.status_code == 302

def test_post_buygame_route_with_session():
    """
    Testing buygame page with user session
    Method : POST
    """
    set_token(client, "usertest")
    response = client.post(url)
    assert response.status_code == 302