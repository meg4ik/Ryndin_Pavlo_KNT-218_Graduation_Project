from src import app, db
from src.database.models import User
import jwt
import datetime

def set_token(client, username):
    server_name = app.config["SERVER_NAME"] or "localhost"
    user =  db.session.query(User).filter(User.username == username).first()
    
    token = jwt.encode(
            {
                "user_id": user.uuid,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm="HS256"
        )
    client.set_cookie(server_name, 'token', token)