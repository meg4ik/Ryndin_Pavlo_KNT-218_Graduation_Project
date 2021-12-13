import datetime
import jwt
from flask_restful import Resource
from flask import flash, make_response, redirect, request, url_for
from flask_restful import Resource
from src import app
from src.database.models import User

class Login(Resource):
    def get(self):
        flash('Method is not allowed', category='danger')
        return redirect(url_for('main'))

    def post(self):

        #take data from responce form
        auth = request.form.to_dict()
        #get user with from key "username"
        user = User.query.filter_by(username=auth.get('username')).first()
        #if user or user hash are not match
        if not user or not user.check_password(auth.get('password')):
            flash('Username and password are not match! Please try again',
                  category='danger')
            #returning redirect login
            return redirect(url_for('main'))
        #make csrf code by jwt algorithm
        hour = 168 if auth.get('remember') else 1
        token = jwt.encode(
            {
                "user_id": user.uuid,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=hour)
            }, app.config['SECRET_KEY'], algorithm="HS256"
        )

        flash('You have been authorized', category='success')
        #set cookie token and return main page
        response = make_response(redirect(url_for('main')))
        response.set_cookie('token', token)
        return response

class Logout(Resource):
    def get(self):
        flash('Method is not allowed', category='danger')
        return redirect(url_for('main'))
    def post(self):
        response = make_response(redirect(url_for('main')))
        response.set_cookie('token', expires=0)
        return response