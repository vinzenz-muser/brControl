import functools

from flask import Blueprint, render_template, flash, redirect, url_for
from admin import db
from admin.models import User
from flask_login import login_required
from admin.forms import AddUserForm, EditUserForm

bp = Blueprint("users", __name__, url_prefix="/admin/users")


@bp.route("/", methods=("GET", "POST"))
@login_required
def showall():
    users = User.query.all()

    form = AddUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, active=1)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you have added a new user!")
        return redirect(url_for("users.showall"))

    return render_template(
        "admin/users/list.html", title="Users", users=users, form=form
    )


@bp.route("/<int:id>/delete", methods=("GET", "POST"))
@login_required
def delete(id):
    deluser = User.query.filter_by(id=id).one()
    db.session.delete(deluser)
    db.session.commit()
    return redirect(url_for("users.showall"))


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit(id):
    edituser = User.query.filter_by(id=id).one()
    form = EditUserForm(obj=edituser)

    if form.validate_on_submit():
        edituser.username = form.username.data
        edituser.set_password(form.password.data)
        db.session.commit()
        flash("Congratulations, you have changed the user!")
        return redirect(url_for("users.showall"))

    return render_template(
        "admin/users/edit.html", title="Edit User", form=form, user=edituser
    )
