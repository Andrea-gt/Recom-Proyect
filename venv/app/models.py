from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from py2neo.ogm import GraphObject, Property

class User(UserMixin, GraphObject):
    __primarylabel__ = "user"
    __primarykey__ = "email"
    name = Property()
    email = Property()
    password = Property()
    hashed_password = Property()