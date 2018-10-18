from flask import Flask
from flask import render_template

app = Flask(__name__)
app.debug = True

@app.route('/')
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
    return render_template("admin_view_user.html")

if __name__ == '__main__':
    app.run(debug=True)
