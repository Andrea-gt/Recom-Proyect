from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from py2neo.ogm import GraphObject, Property
from passlib.handlers.sha2_crypt import sha512_crypt as crypto


class User(UserMixin, GraphObject):
    __primarylabel__ = "user"
    __primarykey__ = "email"
    username = Property()
    name = Property()
    age = Property()
    email = Property()
    password = Property()
    hashed_password = Property()
