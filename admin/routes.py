from admin import app

@app.route('/hello')
def hello():
    return 'hello world'

@app.route('/dashboard/', defaults={'path': ''})
def static_dash(path):
    print("Here")
    return app.send_static_file("dash/index.html")