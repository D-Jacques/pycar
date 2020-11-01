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

        
#We registers users here
@app.route('/register', methods=['POST', 'GET'])
def register():
    #If we send a form with the register.html page we fit the condition
    if request.method == 'POST':
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
        #We execute the query, if it found something, it means a user already 
        #took the username
        elif db_connect.execute(
            'SELECT id FROM pycar_user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'Ce nom d\'utilisateur est déjà utilisé !'
        elif db_connect.execute(
            'SELECT id FROM pycar_user WHERE user_mail = ?', (email,)
        ).fetchone() is not None:
            error = 'l\'adresse mail est déjà utilisée!'
        if error is None:
            db_connect.execute(
                'INSERT INTO pycar_user(username, user_password, user_mail) VALUES (?, ?, ?)',
                (username,generate_password_hash(password), email)
            )
            db_connect.commit()
            flash('Le compte est désormais inscri, vous pouvez vous connecter')
            #The user is redirected to the connection page
            return redirect(url_for('connection'))
        
        flash(error)

    return render_template('register.html')

<<<<<<< HEAD
#It's the route for our main page, the user have to connect
#with his logs to get farther
@app.route('/connection', methods=['POST', 'GET'])
def connection():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_user = db.get_db()
        error = None
        checkUser = db_user.execute(
            'SELECT * FROM pycar_user WHERE username = ?',
            (username,)
        ).fetchone()
        if checkUser is None:
            error = 'Erreur : le nom d\'utilisateur renseigné n\'existe pas !'
        elif not check_password_hash(checkUser['user_password'], password):
            error = 'Erreur : Le mot de passe renseigné est incorrect pour cet utilisateur'
        if error is None:
            session.clear()
            session['username'] = checkUser['username']
            session['id'] = checkUser['id']
            return redirect(url_for('index'))
        
        flash(error)
    return render_template('connection.html')

=======
  #Adding cars to the DataBase
    @app.route('/AjoutVoiture', methods=('GET','POST'))
        def AddCar():
            if request.method == 'POST':
                carname  = request.form['carname']
                carbrand = request.form['carbrand']
                carprice = request.form['carprice'] 
                db_connect = db.get_db()
                error = None

                    if not carname:
                        error = 'carname is required.'
                    elif not carbrand:
                         error = 'carbrand is required.'
                    elif not carprice:
                         error = 'carprice is required.'

                    
                    if error is None:
                        db_connect.execute(
                            'INSERT INTO pycar_cars (car_name, car_brand,car_price) VALUES (?, ?, ?)',
                            (carname, carbrand, carprice)
                        )
                        db_connect.commit()
                        return redirect(url_for('Voiture'))


>>>>>>> 170dd41dcb43074527729618b62f5f0060b2e8a3
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('id', None)
    flash('Vous vous êtes déconnecté !')
    return redirect(url_for('connection'))

#We check if a session is set with a username
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


#Adding cars to the DataBase
# @app.route('/AjoutVoiture', methods=('GET','POST'))
# def AddCar():
#     if request.method == 'POST':
#         carname  = request.form['carname']
#         carbrand = request.form['carbrand']
#         carprice = request.form['carprice'] 
#         db_connect = db.get_db()
#         error = None

#         if not carname:
#             error = 'carname is required.'
#         elif not carbrand:
#                 error = 'carbrand is required.'
#         elif not carprice:
#                 error = 'carprice is required.'

        
#         if error is None:
#             db_connect.execute(
#                 'INSERT INTO pycar_cars (car_name, car_brand,car_price) VALUES (?, ?, ?)',
#                 (carname, carbrand, carprice)
#             )
#             db_connect.commit()
#         return redirect(url_for('Voiture'))

@app.route('/index/car_board_seller')
def car_board_seller():
    db_cars = db.get_db()
    cars_data = db_cars.execute(
        'SELECT * FROM pycar_cars'
    ).fetchall()

    return render_template('carboard_seller.html', cars = cars_data)

@app.route('/index/modify_car/<id_car>', methods=['POST', 'GET'])
def car_modification(id_car=None):
    db_cars = db.get_db()
    car_selected = db_cars.execute(
        'SELECT * FROM pycar_cars WHERE id = ?',
        (id_car,)
    ).fetchone()

    if car_selected is None:
        error = 'La voiture que vous voulez modifier n\'existe pas !'
        flash(error)
        return redirect(url_for('car_board_seller'))
    
    return render_template('modify_car.html', cars=car_selected)

#Customisation of 404 page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404