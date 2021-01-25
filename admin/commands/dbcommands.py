from admin import app
from admin import db
from admin.models import Device, Sensordata
import secrets
import click
import datetime


@app.cli.command("clean-data")
def clean_data():
    keep_all_for = datetime.timedelta(days=1)
    periodicity = datetime.timedelta(minutes=5)
    now = datetime.datetime.utcnow()
    start = now - keep_all_for

    all_data = Sensordata.query.filter(Sensordata.time < start).order_by(Sensordata.time.desc()).all()
    last_saved = None
    for data in all_data:
        if not last_saved:
            last_saved = data.time
        
        if data.time > last_saved - periodicity:
            db.session.delete(data)
        else:
            last_saved = data.time

    db.session.commit()