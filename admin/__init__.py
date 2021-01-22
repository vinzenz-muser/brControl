import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, user_logged_in, user_logged_out, user_login_confirmed
from flask_socketio import SocketIO
import flask_socketio
import engineio          
import socketio

print("flask-socketio version: ", flask_socketio.__version__)
print("python_engineio version: ", engineio.__version__)
print("python_socketio version: ", socketio.__version__)

app = Flask(__name__, instance_relative_config=True)

app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins="*", cookie=False)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.session_protection = "strong"
login.login_view = 'auth.login'

from admin import routes, models, forms
from admin.commands import usercommands, devicecommands
from admin.blueprints import users, devices, auth, socket

app.register_blueprint(auth.bp)
app.register_blueprint(users.bp)
app.register_blueprint(devices.bp)
app.register_blueprint(socket.bp)
