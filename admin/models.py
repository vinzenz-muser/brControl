import datetime
from admin import db


class Device(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    location = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)    


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deviceId = db.Column(db.String(64), db.ForeignKey('device.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Sensor {} from device {}>'.format(self.name, self.deviceId)    


class Sensordata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensorId = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    value = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return '<Sensordata {} from sensor {}>'.format(self.id, self.sensorId)    


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.Binary(64), nullable=False)
    active = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)    
