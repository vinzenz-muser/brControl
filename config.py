import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///./database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST="0.0.0.0"
    DEBUG=os.environ.get('DEBUG') or False
    ENV=os.environ.get('FLASK_ENV') or "production"
    SESSION_COOKIE_SECURE=os.environ.get('FLASK_SESSION_COOKIE_SECURE') or True
    USER=os.environ.get('SENSOR_USER')
    DATA_HANDLER=dict()
    DATA_HANDLER["provider"] = os.environ.get('DATA_PROVIDER') or "sql"

    if DATA_HANDLER["provider"] == "influx":
        DATA_HANDLER["config"] = {
            "token": os.environ.get('INFLUX_TOKEN'),
            "url": os.environ.get('INFLUX_URL'),
            "org": "brauradau",
            "buckets": {
                "rt": os.environ.get('SENSOR_USER')+"_rt",
                "1m": os.environ.get('SENSOR_USER')+"_1m",
                "5m": os.environ.get('SENSOR_USER')+"_5m"
            },
            "base": os.environ.get('SENSOR_USER')
        }
