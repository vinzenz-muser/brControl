import functools

from flask import Blueprint, render_template
from admin import db
from flask_login import login_required

bp = Blueprint('devices', __name__, url_prefix='/admin/devices')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def showall():
    return render_template('admin/devices.html', title='Devices')