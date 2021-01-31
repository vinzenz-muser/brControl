from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for, make_response)
from admin.models import User, Sensor, Device
from admin import app, socketio, producer

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
        sensors = device.sensors.all()
        data[device.id] = {
            "id": device.id,
            "type": device.type,
            "device": device.name,
            "location": device.location,
            "active": False,
            "sensors": {s.id: s.to_dict() for s in sensors},
        }
        
    emit(
        "update_sensors", 
        data, 
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

    