from flask import Flask
from app.db_session import db_auth
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

app = Flask(__name__)
app.config.from_object(Config)
graph = db_auth()

from app import routes