import functools
from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3, os

bp_admin = Blueprint('admin', __name__)

#generate secret key
secret_key = os.urandom(10)
app.config.update(
    TESTING=True,
    SECRET_KEY=secret_key)

@bp_admin.route('/admin', methods=['POST'])
def admin_main():
    if request.method == 'POST':
        email = request.form['txtEmail']
        password = request.form['txtPass']
        db = sqlite3.connect('epitome.db')
        reader = db.cursor()
        q = "SELECT * FROM Users WHERE is_deleted = 0 AND type = 1 AND email = ? AND password = ?"
        reader.execute(q, (email, password))
        dataReader = reader.fetchone()
        print("email = " + email)
        if(dataReader is None):
            return render_template("login.html", prompt="Invalid credentials. Try Again!")
        else:
            if(dataReader[3] == email and dataReader[5] == password):
                db.commit()
                db.close()

                first=dataReader[1]
                last=dataReader[2]
                session['userID'] = str(dataReader[0])
                sID = str(session['userID']) + str(app.secret_key)
                x = render_template('admin_add_item.html')

    return x




def displayRecord_FA(tbl):
    q = "SELECT * FROM %s WHERE is_deleted = 0 LIMIT 10" % (tbl)
    db = sqlite3.connect('epitome.db')
    reader = db.cursor()
    reader.execute(q)
    read = reader.fetchall()
    return read

def displayRecord_FO(tbl):
    q = "SELECT * FROM %s WHERE is_deleted = 0 LIMIT 10" % (tbl)
    db = sqlite3.connect('epitome.db')
    reader = db.cursor()
    reader.execute(q)
    read = reader.fetchone()
    return read

def displayRecord_WF(tbl, filter, p):
    q = "SELECT * FROM %s WHERE is_deleted = 0 AND %s" % (tbl, filter)
    db = sqlite3.connect('epitome.db')
    reader = db.cursor()
    reader.execute(q, p)
    read = reader.fetchall()
    return read

def simple_execution(q, p):
    db = sqlite3.connect('epitome.db')
    reader = db.cursor()
    reader.execute(q, (p))
    db.commit()
    db.close()