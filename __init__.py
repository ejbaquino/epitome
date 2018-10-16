from flask import Flask
from flask import render_template

app = Flask(__name__)
app.debug = True

@app.route('/')
def landing():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)