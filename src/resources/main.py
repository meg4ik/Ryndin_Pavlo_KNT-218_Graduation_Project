from flask import make_response, render_template, request
from flask_restful import Resource
from src.token import get_user_by_token
from src.database.models import User, Role

class Main(Resource):

    def get(self):
        try:
            user = get_user_by_token()
        except:
            # return page with no user session
            return make_response(render_template("main.html",), 200)
        # return page in user session
        role = Role.query.join(User).filter_by(username=user.username).first()
        return make_response(render_template("main.html", user=user, user_code=role.code), 202)