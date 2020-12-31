import functools

from flask import Blueprint, render_template
from admin import db
from admin.models import User
from flask_login import login_required
from admin.forms import RegistrationForm

bp = Blueprint('users', __name__, url_prefix='/admin/users')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def showall():
    users = User.query.all()
    return render_template('admin/users/list.html', title='Users', users=users)


@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):
    deluser = User.query.filter_by(id=id).one()
    db.session.delete(deluser)
    db.session.commit()
    return redirect(url_for('admin.users.showall'))

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    deluser = User.query.filter_by(id=id).one()
    db.session.delete(deluser)
    db.session.commit()
    return redirect(url_for('admin.users.showall'))

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    deluser = User.query.filter_by(id=id).one()
    db.session.delete(deluser)
    db.session.commit()
    return render_template('admin/users/create.html', title='Create User', form=RegistrationForm)