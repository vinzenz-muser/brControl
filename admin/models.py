import datetime
from admin import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    apiKey = db.Column(db.String(64), nullable=False, unique=True)
    sensors = db.relationship('Sensor', backref='device', lazy='dynamic', cascade="all, delete-orphan")
    type = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<User {self.id} Type {self.type}>'

    def set_api_key(self):
        token = secrets.token_urlsafe(32)
        self.apiKey = token


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deviceId = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    datapoints = db.relationship('Sensordata', backref='sensor', lazy='dynamic', cascade="all, delete-orphan")
    target = db.Column(db.Float, nullable=True)
    accuracy = db.Column(db.Float, nullable=True)
    suffix = db.Column(db.String(32), nullable=False, server_default="°C")

    def __repr__(self):
        return f'<Sensor {self.name} from device {self.deviceId}>'


class Sensordata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensorId = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Sensordata {self.id} from sensor {self.sensorId}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    active = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User {self.username}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))