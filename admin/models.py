import datetime
from admin import db, login, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import pandas as pd
import requests
import json
import numpy as np
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

    def __repr__(self):
        return f'<Sensor {self.name} from device {self.deviceId}>'

    def to_dict(self):
        ans = {
            key: value for key, value in self.__dict__.items() if key in self.__table__.columns.keys()
        }
        req_id = f"{app.config['USER']}_{self.deviceId}_{self.id}"
        now = datetime.datetime.utcnow()
        start = 1000*int((now - datetime.timedelta(minutes=60)).timestamp())

        url = app.config['KSQL_URL']+"/query"
        request_strings = {
            "1m": {
                "db": "AVERAGES_1_MINUTE",
                "start": 1000*int((now - datetime.timedelta(minutes=60)).timestamp())
            },
            "1h": {
                "db": "AVERAGES_1_HOUR",
                "start": 1000*int((now - datetime.timedelta(hours=120)).timestamp())
            },
            "1d": {
                "db": "AVERAGES_1_DAY",
                "start": 1000*int((now - datetime.timedelta(days=60)).timestamp())
            },
        }
        plot_data = dict()
        for interval, conf in request_strings.items():
            plot_data[interval] = {
                "values": [],
                "timestamps": []
            }

            ksql_request = {
                "ksql": f"SELECT WINDOWSTART, WINDOWEND, AVERAGE FROM {conf['db']} WHERE ID='{req_id}' AND WINDOWSTART > {conf['start']};"
            }

            response = requests.post(url, data = json.dumps(ksql_request)).json()
            try:
                for row in response[1:]:
                    plot_data[interval]["values"].append(row['row']['columns'][2])

                    timestamp = row['row']['columns'][1] / 1000
                    timestring = datetime.datetime.fromtimestamp(timestamp).strftime("%H:%M")
                    plot_data[interval]["timestamps"].append(timestring)
            except TypeError:
                print("No cool response")

        ans["plot_data"] = plot_data

        ksql_request = {
            "ksql": f"SELECT VALUE, ACCURACY FROM TARGET_TABLE WHERE ID='{req_id}';"
        }

        response = requests.post(url, data = json.dumps(ksql_request)).json()

        try:
            current = response[1]
            ans["target"] = current["row"]["columns"][0]
            ans["accuracy"] = current["row"]["columns"][1]
        except IndexError:
            print("No target / accuracy")

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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))