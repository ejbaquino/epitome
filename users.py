import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

bp = Blueprint('users', __name__)
v = ""

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register', methods=('GET','POST'))
#@login_required
def register():
    if request.method == 'POST':
        firstn = request.form['firstName']
        lastn = request.form['lastName']
        eml = request.form['inputEmail']
        un = request.form['inputUsername']
        pw = request.form['inputPassword']
        cpw = request.form['confirmPassword']

        if pw != cpw:
            return '<script> alert("Password must be same with the confirm password!") </script>'
        else:
            conn = sqlite3.connect("epitome.db")
            cur = conn.cursor()
            cur.execute(
                    'INSERT INTO USERS (firstname, lastname, email, username, password, type, display)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (firstn, lastn, eml, un, pw, 2, "yes")
            )
            conn.commit()

        return redirect(url_for('users.register'))
    return render_template('register.html')