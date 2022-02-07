from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src.token import get_user_by_token, token_required, get_games
from src.database.models import User, GenreSubgenre, GameGenreSubgenre, Genre, Subgenre, Comment
from src.database.models import Game as GameModel
from src import db
from src.aws_func import get_aws_image

class Game(Resource):
    def get(self, uuid):
        try:
            game_obj = db.session.query(GameModel).filter_by(uuid = uuid).first()
            if not uuid or not game_obj:
                #return main page
                flash("Not such a game",category='danger')
                return redirect(url_for('main'))
            if not game_obj.is_visible or game_obj.is_delete:
                flash("Not such a game",category='danger')
                return redirect(url_for('main'))
            #create genre subgenre dict
            gen_sub = db.session.query(Genre).join(GenreSubgenre).join(GameGenreSubgenre).filter_by(game_id=game_obj.id).all()
            dict_genre_subgenre = {}
            for i in gen_sub:
                subgenres =  db.session.query(Subgenre).join(GenreSubgenre).filter_by(genre_id = i.id).join(GameGenreSubgenre).filter_by(game_id=game_obj.id).all()
                dict_genre_subgenre[i] = list(map(lambda x: x ,subgenres))
            #compose game comments
            user_comment = []
            comments = db.session.query(Comment).filter_by(game_id_from = game_obj.id).all()
            for i in comments:
                date = str(i.created_date)[0:-3]
                user = db.session.query(User).filter_by(id=i.user_id_from).first()
                user_comment_list = []
                user_comment_list.append(user)
                user_comment_list.append(i)
                user_comment_list.append(date)
                user_comment.append(user_comment_list)
            cart_count = len(get_games())
            img_tag = get_aws_image("gamestorebucket", game_obj.uuid)

        except:
            flash('Something went wrong!', category='warning')
            return redirect(url_for('main'))
        #get user and user image
        try:
            user = get_user_by_token()
            try:
                user_icon = get_aws_image("gamestoreuserbucket", user.uuid)
            except:
                user_icon=False
        except:
            return make_response(render_template("game.html", dict_genre_subgenre = dict_genre_subgenre, game = game_obj, user_comment = user_comment, cart_count=cart_count, image=img_tag), 200)
        #retuen page with user session
        return make_response(render_template("game.html",user=user, game = game_obj, dict_genre_subgenre=dict_genre_subgenre, user_comment = user_comment,cart_count=cart_count, image=img_tag, user_icon=user_icon), 202)

    @token_required
    def post(self, uuid):
        user = get_user_by_token()
        game_obj = db.session.query(GameModel).filter_by(uuid = uuid).first()
        if not uuid or not game_obj:
                #return main page
                flash("Not such a game",category='danger')
                return redirect(url_for('main'))
        #add comment
        try:
            content = request.form.to_dict()
            reply_to_message_uuid = content.get('reply_to_message_uuid')
            reply_to_message_id=None
            if reply_to_message_uuid:
                rep_com = db.session.query(Comment).filter_by(uuid=reply_to_message_uuid).first()
                reply_to_message_id = rep_com.id
            #add comment
            com = Comment(
                text=content.get('comment'),
                reply_to_message_id=reply_to_message_id,
                user_id_from=user.id,
                game_id_from=game_obj.id
            )
            db.session.add(com)
            db.session.commit()
            db.session.close()
        except:
            flash('Something went wrong!', category='warning')
        return redirect(url_for('game', uuid=uuid))
        
        


