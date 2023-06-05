import functools

from flask import Blueprint, render_template, flash, redirect, url_for
from admin import db
from flask_login import login_required
from admin.models import Device, Sensor
from admin.forms import AddDeviceform, AddSensorForm

bp = Blueprint("devices", __name__, url_prefix="/admin/devices")


@bp.route("/", methods=("GET", "POST"))
@login_required
def showall():
    form = AddDeviceform()
    devices = Device.query.all()

    if form.validate_on_submit():
        device = Device(location=form.location.data, name=form.name.data)
        device.set_api_key()
        db.session.add(device)
        db.session.commit()
        flash("Congratulations, you have added a new device!")
        return redirect(url_for("devices.showall"))

    return render_template(
        "admin/devices/list.html", title="Devices", devices=devices, form=form
    )


@bp.route("/<int:id>/detail", methods=("GET", "POST"))
@login_required
def detail(id):
    device = Device.query.filter_by(id=id).one()
    sensors = device.sensors.all()
    form = AddDeviceform(obj=device)

    if form.validate_on_submit():
        device.location = form.location.data
        device.name = form.name.data
        db.session.commit()
        flash("Device has been updated.")
        return redirect(url_for("devices.detail", id=id))

    return render_template(
        "admin/devices/detail.html",
        title="Device detail",
        device=device,
        sensors=sensors,
        form=form,
        sensorform=AddSensorForm(),
    )


@bp.route("/<int:id>/refreshapi", methods=("GET", "POST"))
@login_required
def refreshapi(id):
    device = Device.query.filter_by(id=id).one()
    device.set_api_key()
    db.session.commit()
    return redirect(url_for("devices.detail", id=id))


@bp.route("/<int:id>/addsensor", methods=("GET", "POST"))
@login_required
def addsensor(id):
    form = AddSensorForm()
    if form.validate_on_submit():
        add_sensor = Sensor(name=form.name.data, deviceId=id)
        db.session.add(add_sensor)
        db.session.commit()
        flash("Sensor has been added.")
        return redirect(url_for("devices.detail", id=id))

    return redirect(url_for("devices.detail", id=id))


@bp.route("/<int:id>/deletesensor/<int:sensorid>", methods=("GET", "POST"))
@login_required
def deletesensor(id, sensorid):
    sensor = Sensor.query.filter_by(id=sensorid).first()
    db.session.delete(sensor)
    db.session.commit()
    return redirect(url_for("devices.detail", id=id))


@bp.route("/<int:id>/modifysensor/<int:sensorid>", methods=("GET", "POST"))
@login_required
def modifysensor(id, sensorid):
    sensor = Sensor.query.filter_by(id=sensorid).first()
    form = AddSensorForm()

    if form.validate_on_submit():
        sensor.name = form.name.data
        sensor.type = form.type.data
        db.session.commit()
        flash("Sensor has been modified.")
        return redirect(url_for("devices.detail", id=id))

    return redirect(url_for("devices.detail", id=id))


@bp.route("/<int:id>/delete", methods=("GET", "POST"))
@login_required
def delete(id):
    device = Device.query.filter_by(id=id).first()
    db.session.delete(device)
    db.session.commit()
    return redirect(url_for("devices.showall"))
