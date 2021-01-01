import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'auth.login'

from admin import routes, models, forms
from admin.commands import usercommands, devicecommands
from admin.blueprints import users, devices, auth

app.register_blueprint(auth.bp)
app.register_blueprint(users.bp)
app.register_blueprint(devices.bp)
