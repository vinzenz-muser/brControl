from admin import app
from admin import db
import click


@app.cli.command("create-sensor")
@click.argument("path")
def create_user(path):
    return 
