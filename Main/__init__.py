from flask import Flask

app = Flask(__name__)
app.debug = True

@app.route('/')

def display():
    return 'Hello this a sample'

if __name__ == '__main__':
    app.run()