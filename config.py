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
    CONFLUENT_BOOSTRAP_SERVERS='pkc-lq8gm.westeurope.azure.confluent.cloud:9092'
    CONFLUENT_USERNAME='L4EKSUL5FZGMMZIN'
    CONFLUENT_PASSWORD='E27Rc0cXduP1TO1a7jRBkIVB+2HgMHj9B0NqSU4wBFbSBGTxUInUVisQH8Vm1uxQ'
    KSQL_URL='http://localhost:8088'