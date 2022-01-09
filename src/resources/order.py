from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src.token import get_user_by_token, token_required, get_games
import re

class Order(Resource):
    @token_required
    def get(self):
        try:
            user = get_user_by_token()
            games = get_games()
            cart_count = len(games)

        except:
            flash('Something went wrong!', category='warning')
            return redirect(url_for('main'))
        return make_response(render_template("order.html",user=user, games = games, cart_count=cart_count), 200)

    @token_required
    def post(self):
        to_flash = []
        try:
            name = request.form.get('name')
            if len(name)>30 or len(name)==0:
                to_flash.append("Name must be less than 30 characters")
            last_name = request.form.get('surname')
            if len(last_name)>30 or len(last_name)==0:
                to_flash.append("Last name be less than 30 characters")
            new_surname = request.form.get('surname')

            new_email = request.form.get('email_address')
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not(re.fullmatch(regex, new_email)):
                to_flash.append("Invalid Email")

            phone = request.form.get('phone')
            if not phone:
                to_flash.append("Invalid Phone")
            payment = request.form.get('payment')
            if payment != "card" and payment != "cash":
                to_flash.append("Invalid payment type")
            comment = request.form.get('comment')
            if comment:
                if len(comment)>300:
                    to_flash.append("Comment be less than 300 characters")

        except Exception as e:
            flash("Something went wrong",category='danger')
            return redirect(url_for('order'))

        if to_flash:
            for num, mess in enumerate(to_flash):
                flash(mess,category='danger')
                if num == 4:
                    break
            return redirect(url_for('order'))
        else:
            flash("The order was completed successfully",category='success')
            response = make_response(redirect(url_for('main')))
            response.set_cookie('gamelist', "")
            return response






