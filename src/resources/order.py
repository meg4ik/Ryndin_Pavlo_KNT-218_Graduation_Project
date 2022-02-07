from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src.token import get_user_by_token, get_games, role_handler
import re
from src.aws_func import get_aws_image

RESOURCE_ROLES = [0, 1]

class Order(Resource):
    @role_handler(RESOURCE_ROLES)
    def get(self):
        try:
            games = get_games()
            cart_count = len(games)
        except:
            flash('Something went wrong!', category='warning')
            return redirect(url_for('main'))

        try:
            #get user and user img
            user = get_user_by_token()
            try:
                user_icon = get_aws_image("gamestoreuserbucket", user.uuid)
            except:
                user_icon=False
        except:
            return make_response(render_template("order.html", games = games, cart_count=cart_count), 200)

        return make_response(render_template("order.html",user=user, games = games, cart_count=cart_count, user_icon=user_icon), 202)

    def post(self):
        to_flash = []
        try:
            #check name
            name = request.form.get('name')
            if len(name)>30 or len(name)==0:
                to_flash.append("Name must be less than 30 characters")
            #check surname
            last_name = request.form.get('surname')
            if len(last_name)>30 or len(last_name)==0:
                to_flash.append("Last name be less than 30 characters")
            #check email
            new_email = request.form.get('email_address')
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not(re.fullmatch(regex, new_email)):
                to_flash.append("Invalid Email")
            #check phone
            phone = request.form.get('phone')
            if not phone:
                to_flash.append("Invalid Phone")
            #check payment type
            payment = request.form.get('payment')
            if payment != "card" and payment != "cash":
                to_flash.append("Invalid payment type")
            #check comment
            comment = request.form.get('comment')
            if comment:
                if len(comment)>300:
                    to_flash.append("Comment be less than 300 characters")

        except:
            flash("Something went wrong",category='danger')
            return redirect(url_for('order'))
        #return page with errors
        if to_flash:
            for num, mess in enumerate(to_flash):
                flash(mess,category='danger')
                if num == 4:
                    break
            return redirect(url_for('order'))
        else:
            #success order
            flash("The order was completed successfully",category='success')
            response = make_response(redirect(url_for('main')))
            response.set_cookie('gamelist', "")
            return response






