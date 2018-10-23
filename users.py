import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

bp = Blueprint('users', __name__)
v = ""


@bp.route('/login')
def login():
    return render_template("login.html")

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

@bp.route('/admin/users')
def searchUsers():
    users = books = displayRecord_WF("Users", "type = ?", (2,))
    return render_template("admin_users.html", users=users)



@bp.route('/admin/users/name', methods=['POST'])
def searchUserName():
    try:
        if request.method == "POST":
            userID = request.form['btn_uid']
            session['choiceUSER'] = userID
            db = sqlite3.connect('epitome.db')
            reader = db.cursor()
            q = "SELECT Books.isbn,title, author, description FROM Books inner join library on library.isbn = books.isbn inner join users on users.user_id = library.user_id WHERE Books.is_deleted = 0 AND users.type = 2 AND users.user_id = ?"
            reader.execute(q, (userID))
            library = reader.fetchall()
            user = displayRecord_WF("Users", "user_id = ?", userID)
            pr=''
            return render_template("admin_view_user.html", userlib=library, y=user, pr=pr)
    except Exception as x:
        return str(x)
    #<script>alert('" + str(x)+ "')</script>



@bp.route('/admin/users/name/Modify', methods=['POST'])
def modifyUser():
    if request.method == 'POST':
        ID = request.form['modUID']
        first = request.form['modFN']
        last = request.form['modLN']
        email = request.form['modEmail']
        un = request.form['modUN']

        simple_execution("UPDATE Users SET firstname = ?, surname = ?, email = ?, user_name = ? WHERE user_id = ?", (first, last, email, un, ID,))

        users = displayRecord_FA("Users")
        return render_template('admin_users.html', users=users)


@bp.route('/admin/users/name/ModPass', methods=['POST'])
def modifyUserPass():
    if request.method == 'POST':

       ID = request.form['modCID']
       Newpass = request.form['modNpass']

       simple_execution("UPDATE Users SET password = ? WHERE user_id = ?", (Newpass, ID,))
       users = displayRecord_FA("Users")
       return render_template('admin_users.html', users=users)




@bp.route('/admin/users/name/Delete/<int:id>', methods=['GET'])
def deleteUser(id):
    if request.method == 'GET':
        ID = id
        simple_execution("UPDATE Users SET is_deleted = 1 WHERE user_id = ?", (ID,))
        users = displayRecord_FA("Users")
        return render_template('admin_users.html', users=users)


@bp.route('/logout')
def logout():
    session.clear()
    return render_template("login.html", prompt="")







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
