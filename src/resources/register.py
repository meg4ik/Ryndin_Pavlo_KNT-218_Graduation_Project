from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src import app, db
from src.database.models import User
import re
from src.token import get_user_by_token


class Register(Resource):

    def get(self):
        try:
            get_user_by_token()
        except:
            return make_response(render_template("register.html", nav=True), 200)
        flash('You already authorized', category='warning')
        return redirect(url_for('main'))
        
    def post(self):
        to_flash = []
        try:
            new_username = request.form.get('username')
            u = db.session.query(User).filter_by(username = new_username).first()
            if u:
                to_flash.append("User with username as \"{}\" already exist".format(new_username))
            if len(new_username)>30:
                to_flash.append("Username must be less than 30 characters")
            new_name = request.form.get('name')
            if len(new_name)>30:
                to_flash.append("Name must be less than 30 characters")
            new_surname = request.form.get('surname')
            if len(new_surname)>30:
                to_flash.append("Surname must be less than 30 characters")

            new_email = request.form.get('email_address')
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not(re.fullmatch(regex, new_email)):
                to_flash.append("Invalid Email")
            e = db.session.query(User).filter_by(email_address = new_email).first()
            if e:
                to_flash.append("User with email as \"{}\" already exist".format(new_email))
            new_password = request.form.get('password')
            if len(new_password) < 5 or len(new_password) > 50:
                to_flash.append("Password must be more than 5 and less than 50 characters")
            new_password_repeat = request.form.get('password_repeat')
            if new_password !=new_password_repeat:
                to_flash.append("Password mismatch")
        except Exception as e:
            print(e)
            flash("Something went wrong",category='danger')
            return redirect(url_for('register'))

        if to_flash:
            for num, mess in enumerate(to_flash):
                flash(mess,category='danger')
                if num == 4:
                    break
            return redirect(url_for('register'))
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