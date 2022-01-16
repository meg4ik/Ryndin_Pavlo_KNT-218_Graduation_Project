from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src.token import get_user_by_token, get_games, token_required
from src.database.models import User, Role, Game, GenreSubgenre, GameGenreSubgenre, Genre, Subgenre
from src import db
from io import BytesIO
from src import aws_client
import base64

class Main(Resource):

    def get(self):
        try:
            games = set()
            content = request.args.to_dict()
            is_genre_game = True
            for i in content:
                if content[i] == "Genre":
                    curr_games = db.session.query(Game).join(GameGenreSubgenre).join(GenreSubgenre).join(Genre).filter_by(title=i[6:]).all()
                    if isinstance(curr_games, list):
                        for j in curr_games:
                            games.add(j)
                        if len(curr_games)==0:
                            is_genre_game = False
                    
                elif content[i] == "Subgenre":
                    curr_games = db.session.query(Game).join(GameGenreSubgenre).join(GenreSubgenre).join(Subgenre).filter_by(title=i[9:]).first()
                    if isinstance(curr_games, list):
                        for j in curr_games:
                            games.add(j)
            if not games and is_genre_game:
                games = db.session.query(Game).all()
                search = request.args.get('search')

                if search:
                    games = db.session.query(Game).filter(Game.title.contains(search)).all()

            game_genre = {}
            for i in games:
                gen_sub = db.session.query(Genre).join(GenreSubgenre).join(GameGenreSubgenre).filter_by(game_id=i.id).all()
                dop_data = []
                genres = ""
                if gen_sub:
                    if len(gen_sub) > 1:
                        genres = "{} / {}".format(gen_sub[0].title, gen_sub[1].title)
                    else:
                        genres = gen_sub[0].title
                dop_data.append(genres)

                a_file = BytesIO()
                aws_client.download_fileobj("gamestorebucket", i.uuid+".jpg", a_file)
                a_file.seek(0)

                str_equivalent_image = base64.b64encode(a_file.getvalue()).decode()
                img_tag = "data:image/png;base64," + str_equivalent_image
                dop_data.append(img_tag)

                game_genre[i] = dop_data
            dict_genre_subgenre = {}
            genres = db.session.query(Genre).all()
            for i in genres:
                subgenres =  db.session.query(Subgenre).join(GenreSubgenre).filter_by(genre_id = i.id).all()
                dict_genre_subgenre[i] = list(map(lambda x: x ,subgenres))
            cart_count = len(get_games())
                
        except:
            # return page with no games
            flash('Something went wrong!', category='warning')
            return make_response(render_template("main.html",games = {}, dict_genre_subgenre = {}), 200)
        try:
            user = get_user_by_token()
        except:
            # return page with no user session
            return make_response(render_template("main.html",games = game_genre, dict_genre_subgenre = dict_genre_subgenre), 200)
        # return page in user session
        role = Role.query.join(User).filter_by(username=user.username).first()
        
        return make_response(render_template("main.html", user=user, user_code=role.code, games = game_genre, dict_genre_subgenre = dict_genre_subgenre, cart_count=cart_count), 202)