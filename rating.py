import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

bp_rating = Blueprint('rating', __name__)







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