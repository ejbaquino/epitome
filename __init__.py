import functools
from flask import (
   Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
import users
import category
import books
import library
import rating
import comments
import sqlite3
import os
app = Flask(__name__)
app.debug = True


app.register_blueprint(users.bp)
#app.register_blueprint(admin.bp_admin)
app.register_blueprint(category.bp_cat)
app.register_blueprint(books.bp_books)
app.register_blueprint(library.bp_library)
app.register_blueprint(rating.bp_rating)
app.register_blueprint(comments.bp_comments)

app.add_url_rule('/login', endpoint='login')
app.add_url_rule('/register', endpoint='register')
app.add_url_rule('/admin/users', endpoint='searchUsers')
app.add_url_rule('/admin/users/name', endpoint='searchUserName')
app.add_url_rule('/admin/users/name/Modify', endpoint='modifyUser')
app.add_url_rule('/admin/users/name/ModPass', endpoint='modifyUserPass')
app.add_url_rule('/admin/users/name/Delete/<int:id>', endpoint='deleteUser')
app.add_url_rule('/logout', endpoint='logout')


#app.add_url_rule('/admin', endpoint='admin_main')

app.add_url_rule('/admin/category', endpoint='searchCategory')


app.add_url_rule('/admin/books', endpoint='searchBooks')
app.add_url_rule('/admin/books/name', endpoint='searchBookName')
app.add_url_rule('/admin/books/name/Delete', endpoint='deleteBook')
app.add_url_rule('/admin/books/name/Edit', endpoint='updateBook')

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


secret_key = os.urandom(10)
app.config.update(
    TESTING=True,
    SECRET_KEY=secret_key)

@app.route('/admin', methods=['POST'])
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


'''@app.route('/')
@app.route('/home')
def landing():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register') 
def register():
    return render_template("register.html")

@app.route('/admin')
def addItems():
    return render_template("admin_add_item.html")

@app.route('/admin/books')
def searchBooks():
    return render_template("admin_books.html")

@app.route('/admin/category')
def searchCategory():
    return render_template("admin_category.html")

@app.route('/admin/users')
def searchUsers():
    return render_template("admin_users.html")

@app.route('/admin/books/name')
def searchBookName():
    return render_template("admin_view_book.html")

@app.route('/admin/users/name')
def searchUserName():
    return render_template("admin_view_user.html")'''

if __name__ == '__main__':
    app.run()
