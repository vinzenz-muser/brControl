from admin import app
from admin import db
from admin.models import User
import click
import hashlib
import bcrypt


@app.cli.command("create-user")
@click.argument("name")
@click.argument("mail")
@click.argument("password")
def create_user(name, mail, password):
    encoded = hashlib.sha256(password.encode('utf-8')).hexdigest()
    salt = bcrypt.gensalt()
    store = bcrypt.hashpw(encoded.encode('utf-8'), salt)
    add_user = User(name=name, email=mail, password=store, active=1)
    db.session.add(add_user)
    db.session.commit()
