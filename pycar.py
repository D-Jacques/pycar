from flask import Flask, render_template, request, make_response, abort, redirect, url_for
from markupsafe import escape
app = Flask(__name__)

#It's the route for our main page, the user have to connect
#with his logs to get farther
@app.route('/connection')
def connection():
    return render_template('hello.html')

#We access this page only if we send a form with POST method,
#then we check if the written username is correct
@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['username']:
            resp = make_response(render_template('index.html', username = request.form['username']))
            resp.set_cookie('username', request.form['username'])
            return resp
    else:
        return redirect(url_for('connection'))

        @app.route('/logout')

@login_required
def logout():
    logout_user()
    if session.get('was_once_logged_in'):
        # prevent flashing automatically logged out message
        del session['was_once_logged_in']
    flash('Vous vous êtes bien deconnecter')
    return redirect('/connection')

@app.errorhandler(404)
def page_not_found():
    return render_template('')