from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src.token import get_user_by_token, get_games, role_handler
from src.aws_func import get_aws_image

RESOURCE_ROLES = [0, 1]

class Carts(Resource):
    @role_handler(RESOURCE_ROLES)
    def get(self):
        try:
            games = get_games()
            game_img = {}
            #carts img
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
        #user img
        try:
            user = get_user_by_token()
            try:
                user_icon = get_aws_image("gamestoreuserbucket", user.uuid)
            except:
                user_icon=False
        except:
            return make_response(render_template("carts.html", games = game_img, total_price = total, cart_count=cart_count), 200)
        #return page with session
        return make_response(render_template("carts.html",user=user, games = game_img, total_price = total, cart_count=cart_count, user_icon=user_icon), 202)

    def post(self):
        try:
            #if delete
            game_uuid = request.form.to_dict().get('delete')
            gamelist = request.cookies.get('gamelist')
            new_game_list = ""
            #delete from cookie list
            if gamelist:
                m = gamelist.split('&')
                for i in m:
                    if i!=game_uuid:
                        if len(new_game_list) ==0:
                            new_game_list=i
                        else:
                            new_game_list+="{}{}".format('&', i)
            #set new cookie list
            response = make_response(redirect(url_for('carts')))
            response.set_cookie('gamelist', new_game_list)
            return response

        except:
            flash('Something went wrong!', category='warning')
            return redirect(url_for('carts'))
