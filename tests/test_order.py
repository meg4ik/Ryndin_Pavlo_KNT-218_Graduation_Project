from src import app

from tests.tokens import set_token

client = app.test_client()
url = '/order'

def test_get_order_route():
    """
    Testing order page with no session
    Method : GET
    """
    response = client.get(url)
    assert response.status_code == 200

def test_get_order_route_with_session():
    """
    Testing order page with session
    Method : GET
    """

    set_token(client, "usertest")

    response = client.get(url)
    assert response.status_code == 202

def test_post_order_route_right_data():
    """
    Testing order page with right data
    Method : POST
    """
    resp_dict = {"name":"Vlad", "surname":"Nikiforov", "email_address":"vla_nik@gmail.com", "phone":"000-00-000", "payment":"card"}
    response = client.post(url, data=resp_dict)
    assert response.status_code == 302