import datetime
from admin import db, login, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import requests
import json
from sqlalchemy.sql import func
import time


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    apiKey = db.Column(db.String(64), nullable=False, unique=True)
    sensors = db.relationship('Sensor', backref='device', lazy='dynamic', cascade="all, delete-orphan")
    type = db.Column(db.String(64), nullable=False, default="default")

    def __repr__(self):
        return f'<Device {self.id} Type {self.type}>'

    def set_api_key(self):
        token = secrets.token_urlsafe(32)
        self.apiKey = token

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deviceId = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    suffix = db.Column(db.String(32), nullable=False, server_default="°C")
    type = db.Column(db.String(32), nullable=False, server_default="reader")
    target = db.Column(db.Float, nullable=True)
    accuracy = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<Sensor {self.name} from device {self.deviceId}>'

    def to_dict(self):
        ans = {
            key: value for key, value in self.__dict__.items() if key in self.__table__.columns.keys()
        }
        return ans

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    active = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Value(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    value = db.Column(db.Float, nullable=False)
    timespan = db.Column(db.String(8), nullable=False, default="point")
    sensorId = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))