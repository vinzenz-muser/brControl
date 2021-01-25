from flask_login import current_user
from flask import request, session
from admin.models import User, Sensor, Device, Sensordata, Cleanup
from admin.commands.dbcommands import clean_data
from flask_socketio import emit, join_room, leave_room
import datetime

from admin import socketio, db


# Sensors 
@socketio.on('connect', namespace='/sensor')
def sensor_connect():
    if "api_key" not in request.args:
        raise ConnectionRefusedError('Please provide an API-Key')
    api_key = request.args.get("api_key")
    device = Device.query.filter(Device.apiKey == api_key).first()

    if device:
        join_room("device_" + str(device.id))
        return True

    return False

@socketio.on('disconnect', namespace='/sensor')
def sensor_disconnect():
    device = Device.query.filter(Device.apiKey == request.args.get("api_key")).first()

    if device:
        emit('device_disconnect', {"id": device.id}, namespace='/dashboard', room="authorized")

@socketio.on('new_data', namespace='/sensor')
def new_data(data):
    device = Device.query.filter(Device.apiKey == request.args["api_key"]).first()
    newest = Sensordata.query.order_by(Sensordata.time.desc()).first()
    found_data = dict()
    now = datetime.datetime.utcnow()
    save_time = datetime.timedelta(seconds=5)

    cleanup_time = datetime.timedelta(days=1)
    last_cleanup = Cleanup.query.order_by(Cleanup.lastCleanup.desc()).first()

    if not last_cleanup or last_cleanup.lastCleanup < now - cleanup_time:
        clean_data()
        cleanup = Cleanup()
        db.session.add(cleanup)

    if device:
        for key, val in data["data"].items():
            current_sensor = Sensor.query.filter(Sensor.id == key).filter(Sensor.deviceId == device.id).first()
            if current_sensor:
                found_data[current_sensor.id] = val
                if (newest is None or newest.time < now - save_time):
                    add_sensor = Sensordata(sensorId = current_sensor.id, time = now, value = val)
                    db.session.add(add_sensor)

        ans = {
            "data": found_data,
            "deviceid": device.id   
        }
        emit('new_data', ans, namespace='/dashboard', room="authorized")
    
    db.session.commit()    
    db.session.remove()
   

@socketio.on('updated_targets', namespace='/sensor')
def updated_targets(data):
    device = Device.query.filter(Device.apiKey == request.args["api_key"]).first()
    if device:
        for current_data in data:
            sensor = device.sensors.filter(Sensor.id == current_data['sensor_id']).first()

            if sensor:
                sensor.accuracy = current_data['accuracy']
                sensor.target = current_data['value']
                ans = sensor.to_dict()

                db.session.commit()

                emit(
                    "update_sensor_values",
                    ans,
                    namespace="/dashboard",
                    room="authorized"
                )
