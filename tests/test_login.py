import src
from src import app

from tests.tokens import set_token
client = app.test_client()
url = '/login'

def test_get_login_route_without_session():
    """
    Testing login page without user session
    Method : GET
    """
    response = client.get(url)
    assert response.status_code == 302


def test_post_login_with_right_data():
    """
    Testing login page with right data
    Method : POST
    """
    resp_dict = {"username":"usertest", "password":"qwerty"}
    response = client.post(url, data = resp_dict)
    assert response.location[-1:] == "/"

def test_post_logout():
    """
    Testing logout page
    Method : POST
    """
    set_token(client, "usertest")

    url = '/logout'
    response = client.post(url, data = {})
    url = '/main'
    response = client.get(url)
    assert response.status_code == 200