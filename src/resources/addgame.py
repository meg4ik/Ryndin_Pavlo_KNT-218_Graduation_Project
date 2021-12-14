from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src import app, db
from src.database.models import User
from src.token import get_user_by_token, token_required, admin_manager_required


class AddGame(Resource):
    #@admin_manager_required
    @token_required
    def get(self):
        try:
            user = get_user_by_token()
        except:
            # return page with no user session
            return make_response(render_template("main.html",), 200)
        return make_response(render_template("addgame.html",user=user), 200)
        
    def post(self):
        name = request.form.get('name')
        description = request.form.get('description')
