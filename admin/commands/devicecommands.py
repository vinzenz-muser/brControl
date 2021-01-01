from admin import app
from admin import db
from admin.models import Device, Sensor
import secrets
import click


@app.cli.command("create-device")
@click.argument("location")
@click.argument("name")
def create_user(name, location):
    add_device = Device(location=location, name=name)
    add_device.set_api_key()

    db.session.add(add_device)
    db.session.commit()
    return 

@app.cli.command("create-sensor")
@click.argument("name")
@click.argument("deviceid")
def create_sensor(name, deviceid):
    add_sensor = Sensor(name=name, deviceId=deviceid)
    db.session.add(add_sensor)
    db.session.commit()
    return 