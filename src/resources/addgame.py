from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src import app, db
from src.database.models import User
from src.token import get_user_by_token, token_required, admin_manager_required

@admin_manager_required
@token_required
class AddGame(Resource):

    def get(self):
        try:
            get_user_by_token()
        except:
            return make_response(render_template("register.html", nav=True), 200)
        flash('You already authorized', category='warning')
        return redirect(url_for('main'))
        
    def post(self):
        pass