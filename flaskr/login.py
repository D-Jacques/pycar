import functools

from flask import (
   flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

@app.route('/test', methods=('GET', 'POST'))
def test():
    return 'You got to this page congrats !'