import secrets
import os
# python wsgi.py --settings=configs.common_debug
DEBUG = False

SECRET_KEY = secrets.token_hex(16)

#export SHEMA_LINK='localhost/game_store'
#AKIA4NV7OW2FEFZ6MYQI
#vwzVV8og3URgl6wmuuo17VFqX5Q+D34lxc7cIagi

database_pass = os.environ["DATABASE_PASS"].split('\'')[1]
shema_link = os.environ["SHEMA_LINK"].split('\'')[1]


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{}@{}'.format(database_pass, shema_link)

SQLALCHEMY_TRACK_MODIFICATIONS = False
