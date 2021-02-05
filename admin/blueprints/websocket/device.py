from flask_login import current_user
from flask import request, session
from admin.models import User, Sensor, Device, Value
import requests
from flask_socketio import emit, join_room, leave_room
import datetime
import json
from admin import socketio, db, app, data_handler


# Sensors 
@socketio.on('connect', namespace='/sensor')
def sensor_connect():
    allowed = False
    
    if "api_key" not in request.args:
        raise ConnectionRefusedError('Please provide an API-Key')
    api_key = request.args.get("api_key")
    device = Device.query.filter(Device.apiKey == api_key).first()

    if device:
        join_room("device_" + str(device.id))
        allowed = True  

    db.session.remove()
    return allowed


@socketio.on('disconnect', namespace='/sensor')
def sensor_disconnect():
    device = Device.query.filter(Device.apiKey == request.args.get("api_key")).first()

    if device:
        emit('device_disconnect', {"id": device.id}, namespace='/dashboard', room="authorized")
    db.session.remove()    

@socketio.on('new_data', namespace='/sensor')
def new_data(data):
    device = Device.query.filter(Device.apiKey == request.args["api_key"]).first()
    db.session.expunge(device)

    if device:
        for key, val in data["data"].items():
            current_sensor = Sensor.query.filter(Sensor.id == key).filter(Sensor.deviceId == device.id).first()

            if current_sensor:
                socket_response = {
                    "device_id": device.id,
                    "sensor_id": current_sensor.id,
                    "value": val,
                }

                data_handler.provider.insert_value(current_sensor.id, val)
                
                emit(
                    "new_data",
                    socket_response,
                    namespace="/dashboard",
                    broadcast=True
                )
            
            db.session.remove()
    db.session.remove()


@socketio.on('updated_targets', namespace='/sensor')
def updated_targets(data):
    device = Device.query.filter(Device.apiKey == request.args["api_key"]).first()
  
    if device:
        for current_data in data:
            sensor = device.sensors.filter(Sensor.id == current_data['sensor_id']).first()

            if sensor:
                sensor.target = current_data['value']
                sensor.accuracy = current_data['accuracy']

                emit(
                    "update_sensor", 
                    {
                        "id": sensor.id,
                        "deviceId": device.id,
                        "target": current_data['value'],
                        "accuracy": current_data['accuracy'],
                    }, 
                    room='authorized',
                    namespace="/dashboard"
                )

    db.session.remove()
