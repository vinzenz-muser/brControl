import datetime
from admin import db, login, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import pandas as pd
import numpy as np
from sqlalchemy.sql import func


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
    datapoints = db.relationship('Sensordata', backref='sensor', lazy='dynamic', cascade="all, delete-orphan")
    target = db.Column(db.Float, nullable=True)
    accuracy = db.Column(db.Float, nullable=True)
    suffix = db.Column(db.String(32), nullable=False, server_default="°C")
    type = db.Column(db.String(32), nullable=False, server_default="reader")

    def __repr__(self):
        return f'<Sensor {self.name} from device {self.deviceId}>'

    def to_dict(self):
        ans = {
            key: value for key, value in self.__dict__.items() if key in self.__table__.columns.keys()
        }

        time_dict = {
            "1m": {
                "diff": datetime.timedelta(minutes=1),
                "n_data": 10,
                "format": "%H:%M:%S"
            },
            "1h": {
                "diff": datetime.timedelta(hours=1),
                "n_data": 20,
                "format": "%H:%M:%S"
            },
            "1d": {
                "diff": datetime.timedelta(days=1),
                "n_data": 30,
                "format": "%H:%M"
            },
            "1w": {
                "diff": datetime.timedelta(weeks=1),
                "n_data": 30,
                "format": "%d.%m.%Y"
            },
            "4w": {
                "diff": datetime.timedelta(weeks=4),
                "n_data": 30,
                "format": "%d.%m.%Y"
            },
            "max": {
                "diff": datetime.timedelta(weeks=12),
                "n_data": 30,
                "format": "%d.%m.%Y"
            }
        }

        max_duration = time_dict["max"]["diff"]

        current_time = datetime.datetime.utcnow()
        start_time = current_time - max_duration
        pandas_res = pd.read_sql(Sensordata.query.filter((Sensordata.time > start_time) & (Sensordata.sensorId == self.id)).order_by(Sensordata.time.desc()).statement, db.session.bind) 
        plot_data = dict()

        for key, val in time_dict.items():
            time_delta = val["diff"] / val["n_data"]
            plot_data[key] = {
                "values": [],
                "timestamps": []
            }
            
            for i in range(val["n_data"]):
                start = current_time - (i+1)*time_delta
                end = current_time - i*time_delta
                time = start + (end-start)/2
                rel_data = pandas_res[(pandas_res["time"] > start) & (end > pandas_res["time"])].mean(skipna=True)["value"]

                if np.isnan(rel_data):
                    rel_data = None

                plot_data[key]["values"].append(rel_data)
                plot_data[key]["timestamps"].append(time.strftime(val["format"]))
                
            plot_data[key]["values"] = plot_data[key]["values"][::-1]
            plot_data[key]["timestamps"] = plot_data[key]["timestamps"][::-1]
        ans["plot_data"] = plot_data
        return ans


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
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))