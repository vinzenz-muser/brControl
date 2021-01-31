import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, user_logged_in, user_logged_out, user_login_confirmed
from confluent_kafka import Producer
from flask_socketio import SocketIO
import flask_socketio
import engineio          
import socketio

app = Flask(__name__, instance_relative_config=True)

app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins="*", cookie=False)

db = SQLAlchemy(app)

producer = Producer({
    'bootstrap.servers': app.config['CONFLUENT_BOOSTRAP_SERVERS'],
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': app.config['CONFLUENT_USERNAME'],
    'sasl.password': app.config['CONFLUENT_PASSWORD'],
})

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

