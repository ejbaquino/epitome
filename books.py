import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

bp_books = Blueprint('books', __name__)

@bp_books.route('/admin/books')
def searchBooks():
    books = displayRecord_FA("Books")
    return render_template("admin_books.html", books=books)



@bp_books.route('/admin/books/name', methods=['POST'])
def searchBookName():

    if request.method == "POST":
        bookID = request.form['btn_book']

        db = sqlite3.connect('epitome.db')
        reader = db.cursor()
        q = "select category FROM Categories inner join Books_Category on Books_Category.category_id = Categories.category_id inner join Books on Books_Category.isbn = Books.isbn WHERE Books.is_deleted = 0 AND Books.isbn = ?"
        reader.execute(q, (bookID))


        category = reader.fetchall()
        books = displayRecord_WF("Books", "isbn = ?", bookID)

    return render_template("admin_view_book.html", cat=category, boo=books, bID=bookID, bTitle=books[0][1], bAut=books[0][2], bDesc=books[0][4])

@bp_books.route('/admin/books/name/Delete', methods=['POST'])
def deleteBook():
    if request.method == "POST":
        bID = request.form['btn_bdelete']
        simple_execution("UPDATE Books SET is_deleted = 1 WHERE isbn = ?", bID)

        #refresh
        books = displayRecord_FA("Books")
        return render_template('admin_books.html', books=books, prompt=" delete record?")


@bp_books.route('/admin/books/name/Edit', methods=['POST'])
def updateBook():
    if request.method == "POST":
        bID = request.form['btn_bedit']
        bTitle = request.form['u_title']
        bAut = request.form['u_author']
        bDesc = request.form['u_desc']
        simple_execution("UPDATE Books SET title = ?, author = ?, description = ? WHERE isbn = ?", (bTitle, bAut, bDesc, bID))
        #refresh
        books = displayRecord_FA("Books")
        return render_template('admin_books.html', books=books)




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