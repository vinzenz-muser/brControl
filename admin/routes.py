from admin import app
from flask import render_template, redirect, url_for
from flask_login import login_required

@app.route('/')
@login_required
def index():
    return redirect(url_for('home'))


@app.route('/admin')
@login_required
def home():
    return render_template('admin/index.html')

@app.route('/control/', defaults={'path': ''})
def static_dash(path):
    return app.send_static_file("dash/index.html")