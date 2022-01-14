from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src.token import get_user_by_token, token_required, get_games
from io import BytesIO
from src import aws_client
import base64

class Carts(Resource):
    @token_required
    def get(self):
        try:
            user = get_user_by_token()
            games = get_games()
            a_file = BytesIO()
            game_img = {}
            for i in games:
                aws_client.download_fileobj("gamestorebucket", i.uuid+".jpg", a_file)
                a_file.seek(0)
                str_equivalent_image = base64.b64encode(a_file.getvalue()).decode()
                img_tag = "data:image/png;base64," + str_equivalent_image
                game_img[i]=img_tag

            total = 0
            for i in games:
                total += i.price
            cart_count = len(get_games())
        except:
            flash('Something went wrong!', category='warning')
            return redirect(url_for('main'))
        return make_response(render_template("carts.html",user=user, games = game_img, total_price = total, cart_count=cart_count), 200)

    @token_required
    def post(self):
        try:
            game_uuid = request.form.to_dict().get('delete')
            gamelist = request.cookies.get('gamelist')
            new_game_list = ""
            if gamelist:
                m = gamelist.split('&')
                for i in m:
                    if i!=game_uuid:
                        if len(new_game_list) ==0:
                            new_game_list=i
                        else:
                            new_game_list+="{}{}".format('&', i)
            response = make_response(redirect(url_for('carts')))
            response.set_cookie('gamelist', new_game_list)
            return response

        except:
            flash('Something went wrong!', category='warning')
            return redirect(url_for('carts'))
