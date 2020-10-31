'''This file will create the 
connection between our 
database and our programm'''

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


#Says to our program, link to the database, 
#the program wants to gather datas from our database
def get_db():

    #If no connection has been made yet to the database we create one
    if 'db' not in g:

        #We use sqlite3 to create the connection
        g.db = sqlite3.connect( 
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    #Here we have the data we're looking for
    return g.db


#When we finished gathering datas from our database
#we use this program to cut the connection between database
#and our app
def close_db(e=None):
    #We close the database when we finished gathering datas
    db = g.pop('db', None)

    if db is not None:
        db.close()

#This function will get our schema file pycar_schema.sql so as to execute
#the SQL commands inside, that will create our two databases pycar_users
#and pycar_cars
def init_db():
    db = get_db()

    #We set our opened file value context in a variable called f as file
    with current_app.open_resource('pycar_schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#We initialise a new function to activate 
#through the terminal called 'init-db
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('The database pycar has been created')

#So as the application use these functions, we have to declare them
def init_app(app):
    #app.teardown_appcontext declaration will automatically call close db
    #while our cli.add_command will allow us to use init-db command in terminal
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
