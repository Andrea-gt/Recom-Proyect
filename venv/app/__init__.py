from flask import Flask
from config import Config
from app.db_session import db_auth

app = Flask(__name__)
app.config.from_object(Config)
graph = db_auth()

from app import routes