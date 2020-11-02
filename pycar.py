import os
import db
from flask import(
     Flask, render_template, request,
     abort, redirect, url_for,
     session, flash, g
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

#Adding cars to the DataBase
@app.route('/add_car', methods=('GET','POST'))
def car_add():
    
    db_connect = db.get_db()
    error = None    
    
    if request.method == 'POST':
        car_name  = request.form['car_name']
        car_brand = request.form['car_brand']
        car_price = request.form['car_price'] 

        if not car_name:
            error = 'Vous ne pouvez pas laisser le nom du modèle vide !'
        elif not car_brand:
            error = 'Vous ne pouvez pas laisser le nom du contructeur vide !'
        elif not car_price:
            error = 'Vous ne pouvez pas laisser le prix vide !'
        
        if error is None:
            db_connect.execute(
                'INSERT INTO pycar_cars (car_name, car_brand, car_price) VALUES (?, ?, ?)',
                (car_name, car_brand, car_price)
                )
            db_connect.commit()
            return redirect(url_for('car_board'))

        flash(error)

    return render_template('add_car.html')
    

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

@app.route('/car_board')
def car_board():
    db_cars = db.get_db()
    cars_data = db_cars.execute(
        'SELECT * FROM pycar_cars'
    ).fetchall()

    return render_template('car_board.html', cars = cars_data)

@app.route('/modify_car/<id_car>', methods=['POST', 'GET'])
def car_modification(id_car=None):
    #Get the car we want to modify, we're finding it by id
    db_cars = db.get_db()
    error = None

    #If we submitted a form
    if request.method == 'POST':
        car_name = request.form['car_name']
        car_brand = request.form['car_brand']
        car_price = request.form['car_price']

        if not car_name:
            error = 'Vous ne pouvez pas laisser le nom du modèle vide !'
        elif not car_brand:
            error = 'Vous ne pouvez pas laisser le nom du contructeur vide !'
        elif not car_price:
            error = 'Vous ne pouvez pas laisser le prix vide !'

        if error is not None:
            flash(error)
        else:
            db_cars.execute(
                'UPDATE pycar_cars SET car_name = ?, car_brand = ?, car_price = ?'
                ' WHERE id = ?',
                (car_name, car_brand, car_price, id_car)
            )
            db_cars.commit()
            flash('Modification effectuée')

    car_selected = db_cars.execute(
        'SELECT * FROM pycar_cars WHERE id = ?',
        (id_car,)
    ).fetchone()

    #If we don't find the car with the given id
    if car_selected is None:
        error = 'La voiture que vous voulez modifier n\'existe pas !'
        flash(error)
        return redirect(url_for('car_board_seller'))
    
    return render_template('modify_car.html', cars=car_selected)

#Customisation of 404 page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404