from flask import Blueprint

bp = Blueprint("socket", __name__)

from admin.blueprints.websocket import dash, device
