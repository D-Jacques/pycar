import os
import db
import functools
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

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('id') is None:
            return redirect(url_for('connection'))

        return view(**kwargs)

    return wrapped_view

        
#We registers users here
@app.route('/register', methods=['POST', 'GET'])
@login_required
def register():
    #If we send a form with the register.html page we fit the condition
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
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
                'INSERT INTO pycar_user(username, user_password, user_mail, user_role) VALUES (?, ?, ?, ?)',
                (username,generate_password_hash(password), email, role)
            )
            db_connect.commit()
            flash('Le compte est désormais inscri, l\'utilisateur peut se connecter avec ce compte')
        
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
            session['role'] = checkUser['user_role']
            return redirect(url_for('index'))
        
        flash(error)
    return render_template('connection.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('id', None)
    flash('Vous vous êtes déconnecté !')
    return redirect(url_for('connection'))

#We check if a session is set with a username
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/page_profil')
@login_required
def page_profil():
    db_user = db.get_db()

    user_datas = db_user.execute(
        'SELECT user_mail FROM pycar_user WHERE id = ?',
        (session['id'],)
    ).fetchone()

    print(user_datas)

    return render_template('page_profil.html', user = user_datas)

@app.route('/change_mail',  methods=['POST', 'GET'])
@login_required
def change_mail():
    db_mail = db.get_db()
    error = None

    user_datas = db_user.execute(
        'SELECT user_mail FROM pycar_user WHERE id = ?',
        (session['id'],)
    ).fetchone()

    if request.method == 'POST':
        mail_user  = request.form['mail_user']
        new_mail_user = request.form['new_mail']
        new_mail_check = request.form['new_mail_check']

        if user_datas['user_mail'] != mail_user:
            error = "Veuillez rentrer votre mot de passe actuel dans le premier champ"
        
        if mail_user == new_mail_user:
            error = "La nouvelle adresse mail ne peut pas être le même que l'ancien"
        elif not new_mail_user:
            error = "Vous devez rentrer votre nouveau mot de passe"
        elif new_mail_user != new_mail_check:
            error = "Vous devez rentrer la même adresse mail dans les deux derniers champs"

        if error is not None:
            flash(error)
        if error is None:
            db_user.execute(
                'UPDATE pycar_user SET user_mail = ?',
                (new_mail_user,)
                )
            db_user.commit()
            flash('Votre adresse mail à été modifiée avec succès !')
            return redirect(url_for('page_profil'))
    
    return render_template('mail_change.html', user = user_datas)

@app.route('/change_password',  methods=['POST', 'GET'])
@login_required
def change_password():
    db_password = db.get_db()
    error = None

    if request.method == 'POST':
        password_user  = request.form['password_user']
        new_password_user = request.form['new_password_user']
        new_password_check = request.form['new_password_check']

        user_datas = db_user.execute(
            'SELECT user_password FROM pycar_user WHERE id = ?',
            (session['id'],)
        ).fetchone()

        if not check_password_hash(user_datas['user_password'], password_user):
            error = "Votre mot de passe est incorrect"

        if password_user == new_password_user:
            error = "Le nouveau mot de passe ne peut pas être le même que l'ancien"
        elif not new_password_user:
            error = "Veuillez rentrer votre nouveau mot de passe"
        elif new_password_user != new_password_check:
            error = "Vous devez rentrer le même mot de passe dans les deux dernier champs"

        if error is not None:
            flash(error)
        
        if error is None:
<<<<<<< HEAD
            db_user.execute(
=======
            db_password.execute(
>>>>>>> a7289aeb841fe08e74f4505ca4aac972124d6b67
                'UPDATE pycar_user SET user_password = ?',
                (generate_password_hash(new_password_user),)
                )
<<<<<<< HEAD
            db_user.commit()
            flash('Votre mot de passe à été modifiée avec succès !')
=======
            db_password.commit()
>>>>>>> a7289aeb841fe08e74f4505ca4aac972124d6b67
            return redirect(url_for('page_profil'))

    return render_template('password_change.html')

#Adding cars to the DataBase
@app.route('/add_car', methods=('GET','POST'))
@login_required
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
                'INSERT INTO pycar_cars (car_name, car_brand, car_price, to_repair) VALUES (?, ?, ?, ?)',
                (car_name, car_brand, car_price, 0)
                )
            db_connect.commit()
            return redirect(url_for('car_board'))

        flash(error)

    return render_template('add_car.html')

#We created one car_board in common for all the users, as the function
#would work the same for every user's role
@app.route('/car_board')
@login_required
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

    #We get all the informations about the car with the id in link
    car_selected = db_cars.execute(
        'SELECT * FROM pycar_cars WHERE id = ?',
        (id_car,)
    ).fetchone()

    #If we don't find the car with the given id
    if car_selected is None:
        error = 'La voiture que vous voulez modifier n\'existe pas !'
        flash(error)
        return redirect(url_for('car_board'))
    
    return render_template('modify_car.html', cars=car_selected)

   
@app.route('/delete_car/<id_car>', methods=['POST'])
@login_required
def car_delete(id_car):
    db_cars = db.get_db()
    error = None
    car_selected = db_cars.execute(
        'SELECT * FROM pycar_cars WHERE id = ?',
        (id_car,)
    ).fetchone()
    
    if car_selected is None:
        error = 'La voiture que vous voulez supprimer n\'existe pas!'
        flash(error)
    else :
        db_cars.execute(
            'DELETE FROM pycar_cars WHERE id = ?', 
            (id_car,)
        )
        db_cars.commit()
        flash("La voiture a bien été supprimé")
    
    return redirect(url_for('car_board'))   

#Creation of a car_sheet for a vehicle
@app.route('/car_create_sheet/<id_car>', methods=['POST', 'GET'])
@login_required
def car_create_sheet(id_car):
    error = None
    file_content = None
    db_cars = db.get_db()

    #We want to show what has been written previously in the car_sheet
    cars_data = db_cars.execute(
        'SELECT car_name FROM pycar_cars WHERE id = ?',
        (id_car,)
    ).fetchone()

    #If the car has not been found, we can't read his file, we add an error 
    #And flash it after redirection 
    if cars_data is None:
        error = 'La voiture d\'id '+id_car+' n\'existe pas !'
        flash(error)
        return redirect(url_for('car_board'))
    
    if os.path.isdir('car_sheets') == False:
        os.mkdir('car_sheets')
    if os.path.isfile("car_sheets/"+cars_data['car_name']+"-"+id_car+".txt"):
        with open("car_sheets/"+cars_data['car_name']+"-"+id_car+".txt", "r+") as car_sheet_file:
            file_content = car_sheet_file.read()


    if request.method == 'POST':
        sheet_content = request.form['sheet_content']

        with open("car_sheets/"+cars_data['car_name']+"-"+id_car+".txt", "a") as car_sheet_file:
            car_sheet_file.write(sheet_content)

        if not sheet_content:
            error = 'La fiche technique ne peut pas être vide !'

        if error is not None:
            flash(error)
            return redirect(url_for('car_board'))

    return render_template('sheet_creation.html', id_car = id_car, file_content = file_content)

#Customisation of 404 page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404
