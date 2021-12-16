from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src import app, db
from src.database.models import User, Genre, GenreSubgenre, Subgenre, Game
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
            title = content["name"]
            if len(title)<2 or len(title)>40:
                to_flash.append("Name must be less than 40 characters")
            description = content["description"]
            if len(title)<2 or len(title)>40:
                to_flash.append("Description must be less than 300 characters")
            price = content["price"]
            if not price.isdecimal():
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
            u = User(
                username=new_username,
                name=new_name,
                surname=new_surname,
                email_address=new_email,
                password=new_password,
                code = 1
            )
            db.session.add(u)
            db.session.commit()
            db.session.close()
            flash("User has been successfully created",category='success')
            return redirect(url_for('main'))