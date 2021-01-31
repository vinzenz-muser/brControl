import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///./database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST="0.0.0.0"
    DEBUG=os.environ.get('DEBUG') or False
    ENV=os.environ.get('FLASK_ENV') or "production"
    SESSION_COOKIE_SECURE=os.environ.get('FLASK_SESSION_COOKIE_SECURE') or True
    USER="brauerei"
    CONFLUENT_BOOSTRAP_SERVERS=os.environ.get('CONFLUENT_BOOSTRAP_SERVERS')
    CONFLUENT_USERNAME=os.environ.get('CONFLUENT_USERNAME')
    CONFLUENT_PASSWORD=os.environ.get('CONFLUENT_PASSWORD')
    KSQL_URL=os.environ.get('KSQL_URL')