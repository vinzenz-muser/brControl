from admin import app
from flask import render_template
from flask_login import login_required

@app.route('/')
@login_required
def index():
    return render_template('admin/index.html')

@app.route('/dashboard/', defaults={'path': ''})
def static_dash(path):
    return app.send_static_file("dash/index.html")