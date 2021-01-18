import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///./database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST="0.0.0.0"
    DEBUG=os.environ.get('DEBUG') or False
    ENV=os.environ.get('FLASK_ENV') or "production"
