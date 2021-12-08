import uuid
from flask_bcrypt import check_password_hash, generate_password_hash
from src import db

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

    def __init__(self, username, name, surname, email_address, password, code):
        self.username = username
        self.name = name
        self.surname = surname
        self.email_address = email_address
        self.password = generate_password_hash(password).decode('utf8')
        self.uuid = str(uuid.uuid4())

        role = db.session.query(Role).filter(Role.code == code).first()
        self.role_id = role.id

    # def __init__(self, title):
    #     self.title = title
    #     if title == "Admin":
    #         self.code = 3
    #     elif title == "Manager":
    #         self.code = 2
    #     else:
    #         self.code = 1

    def __repr__(self):
        return f'User({self.surname}, {self.name})'

    def check_password(self, attempted_password):
        """
        Compare passwords hash
        return bool
        """
        return check_password_hash(self.password, attempted_password)

    def save_to_db(self):
        """
        add and save user obj
        """
        db.session.add(self)
        db.session.commit()
        db.session.close()

# class Project(db.Model):
#     """
#     Project model
#     """
#     __tablename__ = 'project'

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(40), nullable=False, unique=True)
#     description = db.Column(db.String(300), nullable=False)
#     uuid = db.Column(db.String(36), unique=True)
#     user_department_role_to = db.relationship("UserProjectRole",backref='department',lazy=True)

#     def __init__(self, title, description):
#         self.title = title
#         self.description = description
#         self.uuid = str(uuid.uuid4())

#     def __repr__(self):
#         return f'Project({self.title})'

#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()
#         db.session.close()
