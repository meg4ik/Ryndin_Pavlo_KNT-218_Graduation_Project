from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_bcrypt import check_password_hash, generate_password_hash
import datetime
import os

app = Flask(__name__)
db = SQLAlchemy(app)

database_pass = os.environ["DATABASE_PASS"].split('\'')[1]
shema_link = os.environ["SHEMA_LINK"].split('\'')[1]

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://db_user:{}@{}'.format(database_pass, shema_link)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class UserGame(db.Model):
    __tablename__ = 'user_game'
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    game_id = db.Column(db.ForeignKey('game.id'), primary_key=True)
    count = db.Column(db.Integer, default=1)

class GameGenreSubgenre(db.Model):
    __tablename__ = 'game_genre_subgenre'
    genre_subgenre_id = db.Column(db.ForeignKey('genre_subgenre.id'), primary_key=True)
    game_id = db.Column(db.ForeignKey('game.id'), primary_key=True)
    
    def __init__(self, genre_subgenre_id, game_id):
        self.genre_subgenre_id = genre_subgenre_id
        self.game_id = game_id

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    text = db.Column(db.String(600), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    reply_to_message_id = db.Column(db.Integer, default=None)
    user_id_from = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    game_id_from = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

    def __init__(self, text, reply_to_message_id, user_id_from, game_id_from):
        self.uuid = str(uuid.uuid4())
        self.text = text
        self.reply_to_message_id = reply_to_message_id
        self.user_id_from = user_id_from
        self.game_id_from = game_id_from

class Role(db.Model):
    """
    Role model
    """
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    code = db.Column(db.Integer, nullable=False)
    user_role_to = db.relationship("User",backref='role',lazy=True)

    def __repr__(self):
        return f'Role({self.title})'

class User(db.Model):
    """
    User model
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),nullable=False, unique=True)
    name = db.Column(db.String(30),nullable=False)
    surname = db.Column(db.String(30),nullable=False)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    uuid = db.Column(db.String(36), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    user_game_to = db.relationship("UserGame", backref='user',lazy=True)

    def __init__(self, username, name, surname, email_address, password, code, uuid):
        self.username = username
        self.name = name
        self.surname = surname
        self.email_address = email_address
        self.password = generate_password_hash(password).decode('utf8')
        self.uuid = uuid

        role = db.session.query(Role).filter(Role.code == code).first()
        self.role_id = role.id

    def __repr__(self):
        return f'User({self.surname}, {self.name})'

    def check_password(self, attempted_password):
        """
        Compare passwords hash
        return bool
        """
        return check_password_hash(self.password, attempted_password)

class Game(db.Model):
    """
    Game model
    """
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    description = db.Column(db.String(1000), nullable=False)
    uuid = db.Column(db.String(36), unique=True)
    is_visible = db.Column(db.Boolean, default = True)
    is_delete = db.Column(db.Boolean, default = False)
    price = db.Column(db.Integer, nullable=False)

    user_game_to = db.relationship("UserGame", backref='game',lazy=True)

    genre_subgenre_to = db.relationship("GameGenreSubgenre", backref='game', lazy=True)

    def __init__(self, title, description, price, is_visible=True, is_delete=False):
        self.title = title
        self.description = description
        self.price = price
        self.uuid = '8c19cafb-1eac-45e2-b089-c6e79b2e6c5e'
        self.is_visible = is_visible
        self.is_delete = is_delete

    def __repr__(self):
        return f'Project({self.title})'


class GenreSubgenre(db.Model):
    """
    GenreSubgenre model
    """
    __tablename__ = 'genre_subgenre'
    id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable=True)
    subgenre_id = db.Column(db.Integer, db.ForeignKey("subgenre.id"), nullable=True)

    genre_subgenre_to = db.relationship("GameGenreSubgenre", backref='genre_subgenre', lazy=True)

    __table_args__ = (db.UniqueConstraint(genre_id, subgenre_id),)

class Genre(db.Model):
    """
    Genre model
    """
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)

    def __repr__(self):
        return f'Genre({self.title})'

class Subgenre(db.Model):
    """
    Genre model
    """
    __tablename__ = 'subgenre'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)

    def __repr__(self):
        return f'Subgenre({self.title})'

def finsert():
    role1 = Role(
        title="Admin",
        code=3
        )
    role2 = Role(
        title="Manager",
        code=2
        )
    role3 = Role(
        title="User",
        code=1
        )

    db.session.add(role1)
    db.session.add(role2)
    db.session.add(role3)

    us1 = User(
        username="admin",
        name="John",
        surname="Bow",
        email_address="meg44mag@gmail.com",
        password="totalmag67",
        uuid='90197dc4-1dd7-4838-8283-4c80fd6f1cfc',
        role_id=db.session.query(Role).filter(Role.title == role1.title).first()
        )
    us2 = User(
        username="usertest",
        name="Abduilov",
        surname="Jijaa",
        email_address="mogg@mail.com",
        password="qwerty",
        uuid='f4685c53-5b46-4106-abfb-9d76c1fcb4cd',
        role_id=db.session.query(Role).filter(Role.title == role3.title).first()
        )

    db.session.add(us1)
    db.session.add(us2)

    
    g1 = Game(
        title='Game1',
        description="Game1",
        price=200,
        is_visible=1,
        is_delete=0
    )

    db.session.add(g1)

    db.session.commit()
    db.session.close()

def insert_run():
    """
    Inserting information into a database
    """
    print("Start inserting")
    try:
        finsert()
    except Exception as e:
        print(e)
    else:
        print("Completed successfully")

insert_run()