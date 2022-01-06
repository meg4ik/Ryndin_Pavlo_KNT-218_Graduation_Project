from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src.token import get_user_by_token, token_required, get_games
from src.database.models import User, Role, GenreSubgenre, GameGenreSubgenre, Genre, Subgenre, Comment
from src.database.models import Game as GameModel
from src import db

class Carts(Resource):
    @token_required
    def get(self):
        try:
            user = get_user_by_token()
            games = get_games()
        except:
            flash('Something went wrong!', category='warning')
            return redirect(url_for('main'))
        return make_response(render_template("carts.html",user=user, games = games), 200)