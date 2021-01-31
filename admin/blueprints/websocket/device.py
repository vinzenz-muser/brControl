from flask_login import current_user
from flask import request, session
from admin.models import User, Sensor, Device
import requests
from flask_socketio import emit, join_room, leave_room
import datetime
import json
from admin import socketio, db, producer, app

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
    
    db.session.remove()

@socketio.on('new_data', namespace='/sensor')
def new_data(data):
    device = Device.query.filter(Device.apiKey == request.args["api_key"]).first()

    if device:
        for key, val in data["data"].items():
            current_sensor = Sensor.query.filter(Sensor.id == key).filter(Sensor.deviceId == device.id).first()
            if current_sensor:
                event = {
                    "device_id": device.id,
                    "sensor_id": current_sensor.id,
                    "value": val,
                    "user": app.config["USER"]
                }

                producer.produce("sensor-values", json.dumps(event).encode('utf-8'))
                
                socket_response = {
                    "device_id": device.id,
                    "sensor_id": current_sensor.id,
                    "value": val,
                }

                ans = {
                    "values": [],
                    "times": []
                }

                try:
                    req_id = f"{app.config['USER']}_{device.id}_{current_sensor.id}"
                    now = datetime.datetime.now()
                    start = 1000*int((now - datetime.timedelta(minutes=120)).timestamp())

                    url = app.config['KSQL_URL']+"/query"

                    ksql_request = {
                        "ksql": f"SELECT WINDOWSTART, WINDOWEND, AVERAGE FROM AVERAGES_1_MINUTE WHERE ID='{req_id}' AND WINDOWSTART > {start};"
                    }

                    response = requests.post(url, data = json.dumps(ksql_request)).json()

                    for row in response[1:]:
                        ans["values"].append(row['row']['columns'][2])
                        timestamp = row['row']['columns'][1] / 1000
                        time = datetime.datetime.fromtimestamp(timestamp).strftime("%H:%M")
                        ans["times"].append(time)

                except requests.exceptions.ConnectionError:
                    print("Failed to connect to KSQL")

                socket_response["1m"] = ans

                emit(
                    "new_data",
                    socket_response,
                    namespace="/dashboard",
                    broadcast=True
                )

    db.session.remove()                                         
   
@socketio.on('updated_targets', namespace='/sensor')
def updated_targets(data):
    device = Device.query.filter(Device.apiKey == request.args["api_key"]).first()
    if device:
        for current_data in data:
            sensor = device.sensors.filter(Sensor.id == current_data['sensor_id']).first()

            if sensor:
                event =  {
                    "id": "_".join([app.config["USER"], str(device.id), str(sensor.id)]),
                    "value": current_data['value'],
                    "accuracy": current_data['accuracy'],
                }

                producer.produce("sensor-targets", json.dumps(event).encode('utf-8'))

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