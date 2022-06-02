from flask import Flask
from config import Config
from app.db_session import db_auth
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
graph = db_auth()
login = LoginManager(app)
login.login_view = 'login'

from app import routes