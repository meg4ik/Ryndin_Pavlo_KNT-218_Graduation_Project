from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src.token import get_user_by_token, token_required, get_games, role_handler
from src.aws_func import get_aws_image

RESOURCE_ROLES = [1]

class Carts(Resource):
    @role_handler(RESOURCE_ROLES)
    @token_required
    def get(self):
        try:
            user = get_user_by_token()
            try:
                user_icon = get_aws_image("gamestoreuserbucket", user.uuid)
            except:
                user_icon=False
            games = get_games()
            game_img = {}
            for i in games:
                img_tag = get_aws_image("gamestorebucket", i.uuid)
                game_img[i]=img_tag

            total = 0
            for i in games:
                total += i.price
            cart_count = len(get_games())
        except:
            flash('Something went wrong!', category='warning')
            return redirect(url_for('main'))
        return make_response(render_template("carts.html",user=user, games = game_img, total_price = total, cart_count=cart_count, user_icon=user_icon), 200)

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
