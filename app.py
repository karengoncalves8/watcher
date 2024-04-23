from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/series')
def series():
    return render_template('series.html')

@app.route('/sign')
def sign():
    return render_template('sign.html')

app.run(debug=True)