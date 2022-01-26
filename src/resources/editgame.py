from flask import make_response, request, flash, redirect, url_for, render_template
from flask_restful import Resource
from src.token import token_required, role_handler, get_user_by_token, get_games
from src.database.models import GameGenreSubgenre, Genre, GenreSubgenre, Subgenre, Game
from src import db
from src.aws_func import upload_img, get_aws_image

class EditGame(Resource):
    RESOURCE_ROLES = [2,3]

    @role_handler(RESOURCE_ROLES)
    @token_required
    def get(self, uuid):
        try:
            user = get_user_by_token()
            try:
                user_icon = get_aws_image("gamestoreuserbucket", user.uuid)
            except:
                user_icon=False
        except:
            # return page with no user session
            return make_response(render_template("main.html",), 200)
        game = db.session.query(Game).filter_by(uuid=uuid).first()
        dict_genre_subgenre = {}
        genres = db.session.query(Genre).all()
        for i in genres:
            subgenres =  db.session.query(Subgenre).join(GenreSubgenre).filter_by(genre_id = i.id).all()
            dict_genre_subgenre[i] = list(map(lambda x: x ,subgenres))
        cart_count = len(get_games())
        return make_response(render_template("editgame.html",user=user, game=game, dict_genre_subgenre = dict_genre_subgenre, cart_count=cart_count, user_icon=user_icon), 200)

    @role_handler(RESOURCE_ROLES)
    @token_required
    def post(self, uuid):
        content = request.form.to_dict()
        to_flash = []
        try:
            title_to = content["name"]
            if len(title_to)<2 or len(title_to)>40:
                to_flash.append("Name must be less than 40 characters")
            description_to = content["description"]
            if len(description_to)<2 or len(description_to)>1000:
                to_flash.append("Description must be less than 300 characters")
            price_to = content["price"]
            if not price_to.isdecimal():
                to_flash.append("Price must be natural number")
            is_visible = True
            if "is_visible" in content.keys():
                is_visible = False

        except:
            flash("Something went wrong",category='danger')
            return redirect(url_for('addgame'))
        if to_flash:
            for num, mess in enumerate(to_flash):
                flash(mess,category='danger')
                if num == 4:
                    break
            return redirect(url_for('addgame'))

        else:
            db.session.query(Game).filter_by(uuid = uuid).update(
                dict(
                    title=title_to,
                    description=description_to,
                    price=price_to,
                    is_visible=is_visible
                )
            )
            db.session.commit()
            game = db.session.query(Game).filter_by(title = title_to).first()
            try:
                image = request.files['img']  # get file
            except:
                pass
            else:
                upload_img(image,game.uuid)
            
            g = db.session.query(GameGenreSubgenre).filter_by(game_id = game.id).all()
            for i in g:
                db.session.delete(i)
            db.session.commit()

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
            flash("Game has been successfully updated",category='success')
            return redirect(url_for('main'))