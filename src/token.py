import jwt
from src import app
from flask import request
from flask import flash, redirect, request, url_for
from src.database.models import User, Role, Game
from functools import wraps

def get_user_by_token():
    token = request.cookies.get('token')
    uuid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])['user_id']
    user = User.query.filter_by(uuid=uuid).first()
    return user

def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        #wrapper of current func

        #take csrf-token from cookies
        token = request.cookies.get('token')
        if not token:
            #returning login page
            flash("Authentication required", category='danger')
            return redirect(url_for('login'))
        #decoding token
        try:
            uuid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])['user_id']
        except:
            #returning login page
            flash("Token timeout", category='danger')
            return redirect(url_for('login'))
        #get current user
        user = User.query.filter_by(uuid=uuid).first()
        if not user:
            #returning login page
            flash("Profile error", category='danger')
            return redirect(url_for('login'))
        return func(self, *args, **kwargs)
    return wrapper
    
def role_handler(roles):
    def dec(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            #wrapper of current func
            try:
                user = get_user_by_token()
                role = Role.query.join(User).filter_by(username=user.username).first()
            except:
                flash("You have no permission for this page!", category='danger')
                return redirect(url_for('main'))
            if not role.code in roles:
                flash("You have no permission for this page!", category='danger')
                return redirect(url_for('main'))
            return func(self, *args, **kwargs)
        return wrapper
    return dec

def get_games():
    g_obj_list = []
    gamelist = request.cookies.get('gamelist')
    if not gamelist:
        return g_obj_list
    m = gamelist.split('&')
    
    for i in m:
        game = Game.query.filter_by(uuid=i).first()
        if game:
            f = True
            for j in g_obj_list:
                if j==game:
                    f=False
                    break
            if f:
                g_obj_list.append(game)
    return g_obj_list
