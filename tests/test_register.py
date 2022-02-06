from src import app, db
from src.database.models import User
from tests.tokens import set_token

client = app.test_client()
url = '/register'

def test_get_register_route():
    """
    Testing register page with no session
    Method : GET
    """
    response = client.get(url)
    assert response.status_code == 200

def test_get_register_route_auth():
    """
    Testing register page with user session
    Method : GET
    """
    set_token(client, "usertest")

    response = client.get(url)
    assert response.status_code == 302

def test_post_login_with_right_data():
    """
    Testing register page with right data
    Method : POST
    """
    resp_dict = {"username":"usertest1", "name":"Vlad", "surname":"Nikiforov", "email_address":"vla_nik@gmail.com", "password":"qwerty", "password_repeat":"qwerty"}
    response = client.post(url, data = resp_dict)
    user = db.session.query(User).filter_by(username = "usertest1").first()
    db.session.delete(user)
    db.session.commit()
    assert response.location[-1:] == "/"