from admin import app
from admin import db
from admin.models import User
import click


@app.cli.command("create-user")
@click.argument("name")
@click.argument("password")
def create_user(name, password):
    add_user = User(username=name, active=1)
    add_user.set_password(password)
    db.session.add(add_user)
    db.session.commit()
