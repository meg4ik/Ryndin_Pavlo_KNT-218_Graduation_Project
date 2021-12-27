from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src import app, db
from src.database.models import GameGenreSubgenre, User, Genre, GenreSubgenre, Subgenre, Game
from src.token import get_user_by_token, token_required, role_handler


class AddGame(Resource):
    RESOURCE_ROLES = [2,3]

    @role_handler(RESOURCE_ROLES)
    @token_required
    def get(self):
        try:
            user = get_user_by_token()
        except:
            # return page with no user session
            return make_response(render_template("main.html",), 200)
        dict_genre_subgenre = {}
        genres = db.session.query(Genre).all()
        for i in genres:
            subgenres =  db.session.query(Subgenre).join(GenreSubgenre).filter_by(genre_id = i.id).all()
            dict_genre_subgenre[i] = list(map(lambda x: x ,subgenres))
        return make_response(render_template("addgame.html",user=user, dict_genre_subgenre = dict_genre_subgenre), 200)
        
    @role_handler(RESOURCE_ROLES)
    @token_required
    def post(self):
        content = request.form.to_dict()
        to_flash = []
        try:
            title_to = content["name"]
            if len(title_to)<2 or len(title_to)>40:
                to_flash.append("Name must be less than 40 characters")
            description_to = content["description"]
            if len(description_to)<2 or len(description_to)>40:
                to_flash.append("Description must be less than 300 characters")
            price_to = content["price"]
            if not price_to.isdecimal():
                to_flash.append("Price must be natural number")
        except Exception as e:
            flash("Something went wrong",category='danger')
            return redirect(url_for('addgame'))
        if to_flash:
            for num, mess in enumerate(to_flash):
                flash(mess,category='danger')
                if num == 4:
                    break
            return redirect(url_for('addgame'))

        else:
            g = Game(
                title=title_to,
                description=description_to,
                price=price_to
            )
            db.session.add(g)
            db.session.commit()
            flash("Game has been successfully created",category='success')
            game = db.session.query(Game).filter_by(title = title_to).first()
            for i in content:
                try:
                    if i[0:5] == "Genre":
                        gs = db.session.query(GenreSubgenre).filter_by(genre_id = content[i], subgenre_id = None).first()
                        a = GameGenreSubgenre(
                            genre_subgenre_id=gs.id,
                            game_id=game.id
                        )
    
                    elif i[0:8] == "Subgenre":
                        gs = db.session.query(GenreSubgenre).filter_by(subgenre_id = content[i]).first()
                        a = GameGenreSubgenre(
                            genre_subgenre_id=gs.id,
                            game_id=game.id
                        )
                    db.session.add(a)
                    db.session.commit()
                except:
                    continue
            db.session.close()
            return redirect(url_for('main'))