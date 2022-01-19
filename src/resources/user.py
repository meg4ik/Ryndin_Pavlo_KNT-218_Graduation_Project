from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from src.token import get_user_by_token, token_required, get_games
from src.database.models import Role
from src.database.models import User as UserModel
from src import db
import re
from flask_bcrypt import generate_password_hash
from src.aws_func import upload_user_img, get_aws_image

class User(Resource):
    @token_required
    def get(self, uuid):
        try:
            user_obj = db.session.query(UserModel).filter_by(uuid = uuid).first()
            if not uuid or not user_obj:
                #return main page
                flash("Not such user",category='danger')
                return redirect(url_for('main'))
            curr_user = get_user_by_token()
            try:
                user_icon = get_aws_image("gamestoreuserbucket", curr_user.uuid)
            except:
                user_icon=False
            role = Role.query.join(UserModel).filter_by(uuid=curr_user.uuid).first()
            roles = db.session.query(Role).all()
            user_view_role = db.session.query(Role).join(UserModel).filter_by(uuid=user_obj.uuid).first()
            cart_count = len(get_games())
            try:
                img_tag = get_aws_image("gamestoreuserbucket", user_obj.uuid)
            except:
                img_tag = False
        except:
            flash('Something went wrong!', category='warning')
            return redirect(url_for('main'))
        return make_response(render_template("user.html",user=curr_user, user_view = user_obj, user_role=role,user_view_role = user_view_role, roles = roles, cart_count=cart_count, image=img_tag, user_icon=user_icon), 200)
    
    @token_required
    def post(self, uuid):
        content = request.form.to_dict()
        to_flash = []
        try:
            new_name = content['name']
            if len(new_name)>30:
                to_flash.append("Name must be less than 30 characters")
            new_surname = content['surname']
            if len(new_surname)>30:
                to_flash.append("Surname must be less than 30 characters")

            new_email = content['email_address']
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not(re.fullmatch(regex, new_email)):
                to_flash.append("Invalid Email")
            e = db.session.query(UserModel).filter_by(email_address = new_email).first()
            user_obj = db.session.query(UserModel).filter_by(uuid = uuid).first()
            if e and e !=get_user_by_token() and e !=user_obj:
                to_flash.append("User with email as \"{}\" already exist".format(new_email))
            p=True
            if 'password' in content.keys() and 'password_repeat' in content.keys():
                if len(content['password'])>0 and len(content['password_repeat'])>0:
                    new_password = request.form.get('password')
                    if len(new_password) < 5 or len(new_password) > 50:
                        to_flash.append("Password must be more than 5 and less than 50 characters")
                    new_password_repeat = request.form.get('password_repeat')
                    if new_password !=new_password_repeat:
                        to_flash.append("Password mismatch")
                else:
                    p=False
            else:
                p=False
            new_code_role = content['role']
            role_obj = db.session.query(Role).filter_by(code=new_code_role).first()
        except:
            flash("Something went wrong",category='warning')
            return redirect(url_for('user', uuid=uuid))
        if to_flash:
            for num, mess in enumerate(to_flash):
                flash(mess,category='danger')
                if num == 4:
                    break
            return redirect(url_for('user', uuid=uuid))
        else:
            db.session.query(UserModel).filter_by(uuid = uuid).update(
                dict(
                    name=new_name,
                    surname=new_surname,
                    email_address=new_email,
                    role_id=role_obj.id
                )
            )
            db.session.commit()

            if p:
                db.session.query(UserModel).filter_by(uuid = uuid).update(
                dict(
                    password=generate_password_hash(new_password).decode('utf8')
                ))
                db.session.commit()

            user = db.session.query(UserModel).filter_by(uuid=uuid).first()
            try:
                image = request.files['img']  # get file
            except:
                pass
            else:
                upload_user_img(image,user.uuid)
            db.session.close()
            flash("User has been successfully updated",category='success')
            return redirect(url_for('user', uuid=uuid))