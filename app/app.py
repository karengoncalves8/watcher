from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# app.config['MYSQL_HOST'] = 'db'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'Watcher'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fatec'
app.config['MYSQL_DB'] = 'watcher'

mysql = MySQL(app)

app.secret_key = 'your secret key'

    # cursor = mysql.connection.cursor()
    # cursor.execute('select * from Users')
    # output = cursor.fetchall()
    # return str(output)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/series')
def series():
    return render_template('series.html')

@app.route('/signIn')
def signIn():
    return render_template('signIn.html')

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    msg = ''
    if request.method == 'POST':
        Name = request.form['Name']
        Email = request.form['Email']
        Password = request.form['Password']
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO Users (Name, Email, Password) VALUES(%s, %s, %s)''', (Name, Email, Password))
        mysql.connection.commit()
        cursor.close()
        msg = 'You have successfully registered !' 
    return render_template('signUp.html', msg = msg)
    
@app.route('/login', methods = ['POST', 'GET'])
def login():
    msg = ''
    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM Users WHERE Email = %s AND Password = %s''', (Email, Password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            session['email'] = account[2]
            msg = f'Logged in successfully! Welcome {session["username"]}'
        else:
            msg = 'Incorrect username / password!'
    return render_template('signIn.html', msg = msg) 

app.run(debug=True)
