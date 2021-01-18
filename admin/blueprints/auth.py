import functools

from admin import app, db
from admin.forms import LoginForm
from admin.models import User
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for, make_response)
from flask_login import current_user, login_user, logout_user, confirm_login
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse
import datetime
import json

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')

    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(next_page)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid name or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)

        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
