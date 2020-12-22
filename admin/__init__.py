import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from admin import routes, models
