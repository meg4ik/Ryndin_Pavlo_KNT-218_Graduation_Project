from flask import make_response, render_template, request, flash
from flask_restful import Resource
from src.token import get_user_by_token
from src.database.models import User, Role, Game, GenreSubgenre, GameGenreSubgenre, Genre
from src import db

class Main(Resource):

    def get(self):
        try:
            games = db.session.query(Game).all()
            game_genre = {}
            for i in games:
                gen_sub = db.session.query(Genre).join(GenreSubgenre).join(GameGenreSubgenre).filter_by(game_id=i.id).all()
                genres = ""
                if len(gen_sub) > 1:
                    genres = "{} / {}".format(gen_sub[0].title, gen_sub[1].title)
                else:
                    genres = gen_sub[0].title
                game_genre[i] = genres
                
        except:
            # return page with no games
            flash('Something went wrong!', category='warning')
            return make_response(render_template("main.html",games = {}), 200)
        try:
            user = get_user_by_token()
        except:
            # return page with no user session
            return make_response(render_template("main.html",games = game_genre), 200)
        # return page in user session
        role = Role.query.join(User).filter_by(username=user.username).first()
        
        return make_response(render_template("main.html", user=user, user_code=role.code, games = game_genre), 202)