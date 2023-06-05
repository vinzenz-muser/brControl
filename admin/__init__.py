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
from admin.datahandler.DataHandler import DataHandler

app = Flask(__name__, instance_relative_config=True)

app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins="*", cookie=False)

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

login = LoginManager(app)
login.session_protection = "strong"
login.login_view = 'auth.login'

provider_config = app.config["DATA_HANDLER"]["config"]
provider_type = app.config["DATA_HANDLER"]["provider"]

from admin import routes, models, forms

if provider_type == "sql":
    provider_config["db"] = db
    provider_config["models"] = models
data_handler = DataHandler(provider_type, provider_config)

from admin.commands import usercommands, devicecommands
from admin.blueprints import users, devices, auth, socket

app.register_blueprint(auth.bp)
app.register_blueprint(users.bp)
app.register_blueprint(devices.bp)
app.register_blueprint(socket.bp)

