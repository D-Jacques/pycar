import os
import db

from flask import(
     Flask, render_template, request,
     make_response, abort, redirect,
     url_for, session, flash, g
)
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY = 'dev',
    DATABASE = os.path.join(app.instance_path, 'pycar.db')
)
#We have to declare this function in our main file so as to enable
#The flask init-db command that will initialise the database
db.init_app(app)

#Function that checks the login wrote in the form
def valid_login(username, password, db_acess):
    if(bool(username)):
        if db_acess.execute(
            'SELECT id FROM pycar_user WHERE username = ?',
            (username,)
        ).fetchone() is not None:
            return username
    else:
        return False

#It's the route for our main page, the user have to connect
#with his logs to get farther
@app.route('/connection', methods=['POST', 'GET'])
def connection():
    if request.method == 'POST':
       if valid_login(request.form['username'], request.form['password'], db.get_db()):
           flash('you were successfully logged in')
           session['username'] = request.form['username']
           return redirect(url_for('index'))
    return render_template('hello.html')

#We access this page only if we send a form with POST method,
#then we check if the written username is correct
@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html', username = session['username'])
    else:
        #Propre ?
        return '''
            <p>Vous ne pouvez pas acceder à cette page sans être authentifié !</p>
            <br>
            <a href=connection> Se connecter </a>
        '''

#We registers users here
@app.route('/register', methods=['POST', 'GET'])
def register():
    #If we send a form with the register.html page we fit the condition
    if request.method == 'POST':
        #We get the values from the form
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        #We open the connection to the database
        db_connect = db.get_db()
        error = None
        
        #The condition wall, if one value is empty, you shall not register
        if not username:
            error = 'Vous devez inscrire un nom d\'utilisateur !'
        elif not password:
            error = 'Vous devez définir un mot de passe pour cet utilisateur !'
        elif not email:
            error = 'Vous devez renseigner un email pour cet utilisateur !'
        #We execute the query, if it found something, it means a user already took the username
        elif db_connect.execute(
            'SELECT id FROM pycar_user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'Un utilisateur avec ce nom d\'utilisateur existe déjà !'
        elif db_connect.execute(
            'SELECT id FROM pycar_user WHERE user_mail = ?', (email,)
        ).fetchone() is not None:
            error = 'Un utilisateur avec ce nom d\'utilisateur existe déjà !'

        #The query here is executed if the form is filled correctly and
        #if the values used for username and mail are not used
        if error is None:
            db_connect.execute(
                'INSERT INTO pycar_user(username, user_password, user_mail) VALUES (?, ?, ?)',
                (username,generate_password_hash(password), email)
            )
            db_connect.commit()

            flash('Le compte est désormais inscri, vous pouvez vous connecter')
            #The user is redirected to the connection page
            return redirect(url_for('connection'))
        
        flash('error')

    return render_template('register.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('connection'))

#Customisation of 404 page
@app.errorhandler(404)
def page_not_found():
    return render_template('page404.html'), 404