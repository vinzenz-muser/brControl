from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for, make_response)
from admin.models import Sensor, Device
from admin import app, socketio, data_handler, db
from datetime import datetime, timedelta

# Users
@socketio.on('connect', namespace='/dashboard')
def dash_connect():
    if current_user.is_authenticated or app.config["ENV"] == "development":
        join_room("authorized")
        if app.config["ENV"] == "development":
            current_user.username = "Anonymous"
            
        ans = {
            "session": request.sid,
            "name": current_user.username
        }
        emit("login_successful", ans, broadcast=True, room=request.sid, namespace='/dashboard')
        
        return True

    else:
        emit("login_failed", broadcast=True, room=request.sid, namespace='/dashboard')
        return False

@socketio.on('update_sensors', namespace='/dashboard')
def dash_update_sensors():
    data = {}
    devices = Device.query.all()
    for device in devices:
        db.session.expunge(device)

    for device in devices:
        sensors = device.sensors.all()
        for sensor in sensors:
            db.session.expunge(sensor)
        db.session.remove()
               
        data[device.id] = {
            "id": device.id,
            "type": device.type,
            "device": device.name,
            "location": device.location,
            "active": False,
            "sensors": {s.id: s.to_dict() for s in sensors},
        }

        for _, sensor in data[device.id]["sensors"].items():
            sensor["plot_data"] = {}

    emit(
        "update_sensors", 
        data, 
        room=request.sid,
        namespace="/dashboard"
    )

@socketio.on('request_sensor_update', namespace='/dashboard')
def get_sensor_data(data):
    sensor_id = data['sensor_id']

    time_deltas = {
        "1m": {
            "delta": timedelta(minutes=60),
            "format": "%H:%M:%S"
        },
        "5m": {
            "delta": timedelta(minutes=300),
            "format": "%H:%M:%S"
        },
        "1h": {
            "delta": timedelta(hours=50),
            "format": "%H:%M:%S"
        },
        "1d": {
            "delta": timedelta(days=50),
            "format": "%d.%m.%y"
        },
    }

    now = datetime.utcnow()
    ans = {
        "device_id": data["device_id"],
        "sensor_id": data["sensor_id"],
        "data": {

        }
    }
    for period in data['periods']:
        try:
            data = data_handler.provider.load_values(sensor_id, period, now-time_deltas[period]["delta"])
            ans["data"][period] = {
                "timestamps": [],
                "values": []
            }
            for res in data:
                ans["data"][period]["timestamps"].append(res[0].strftime(time_deltas[period]["format"]))
                ans["data"][period]["values"].append(res[1])
        except KeyError:
            print("Time period not configured")
        
        emit("update_plot_data",
            ans,
            room=request.sid,
            namespace="/dashboard"
        )
    

@socketio.on('set_targets', namespace='/dashboard')
def dash_set_target(data):
    target_id = data["device_id"]
    
    if target_id:
        emit(
            "update_controller",
            data,
            broadcast=True,
            room="device_"+str(target_id),
            namespace="/sensor"
        )

    