import secrets
import os

#DEBUG = False изменить
DEBUG = False

SECRET_KEY = secrets.token_hex(16)

#set SHEMA_LINK='localhost/game_store'

database_pass = os.environ["DATABASE_PASS"].split('\'')[1]
shema_link = os.environ["SHEMA_LINK"].split('\'')[1]


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{}@{}'.format(database_pass, shema_link)

SQLALCHEMY_TRACK_MODIFICATIONS = False
