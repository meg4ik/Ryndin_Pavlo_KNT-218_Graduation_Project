from flask import make_response, render_template, request
from flask_restful import Resource
from src.token import get_user_by_token


class Main(Resource):

    def get(self):
        try:
            user = get_user_by_token()
        except:
            # return page with no user session
            return make_response(render_template("main.html",), 200)
        # return page in user session
        return make_response(render_template("main.html", user=user), 202)