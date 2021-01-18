from flask import Blueprint

bp = Blueprint('socket', __name__)

from admin.blueprints.socketroutes import dash, device