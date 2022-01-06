from re import T
from flask import make_response, request, flash, redirect, url_for
from flask_restful import Resource
from src.token import token_required
from src import db

class BuyGame(Resource):
    @token_required
    def post(self):
        try:
            game_uuid = request.form.to_dict().get('game')
            gamelist = request.cookies.get('gamelist')
            if not gamelist:
                gamelist=game_uuid
            else:
                m = gamelist.split('&')
                f = True
                for i in m:
                    if i == game_uuid:
                        f=False
                        break
                if f:
                    gamelist+="{}{}".format('&', game_uuid)

            response = make_response(redirect(url_for('carts')))
            response.set_cookie('gamelist', gamelist)
            return response

        except:
            flash('Something went wrong!', category='warning')
            return redirect(url_for('main'))
