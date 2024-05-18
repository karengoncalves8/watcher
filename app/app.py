from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'Watcher'
 
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# # app.config['MYSQL_PASSWORD'] = 'fatec'
# app.config['MYSQL_DB'] = 'watcher'

mysql = MySQL(app)

app.secret_key = 'watcher#01'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/series')
def series():
    return render_template('series.html')

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html')

@app.route('/profile')
def profile(msg=''):
    cur = mysql.connection.cursor()
    id = session['id']
    cur.execute(f'SELECT * FROM Users WHERE CodUser = {id}')
    profile = cur.fetchall()
    cur.close()
    if profile:
        return render_template('profile.html', profile=profile[0], msg=msg)
    else:
        session['loggedin'] = False
        return redirect(url_for('index'))

@app.route('/register', methods = ['POST', 'GET'])
def register():
    msgRegister = ''
    if request.method == 'POST':
        Name = request.form['Name']
        Email = request.form['Email']
        Password = request.form['Password']
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('''INSERT INTO Users (Name, Email, Password) VALUES(%s, %s, %s)''', (Name, Email, Password))
            mysql.connection.commit()
            cursor.close()
            msgRegister = 'You have successfully registered !' 
        except MySQLdb.Error as e:
            if str(e) == '''(1062, "Duplicate entry 'zendaya@gmail.com' for key 'Email'")''':
                msgRegister = 'This email is alredy registered.'
                return render_template('signUp.html', msg = msgRegister)
    return render_template('signUp.html', msg = msgRegister)
    
@app.route('/login', methods = ['POST', 'GET'])
def login():
    msgLogin = ''
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
            msgLogin = f'Logged in successfully! Welcome {session["username"]}'
        else:
            msgLogin = 'Incorrect username / password!'
    return render_template('index.html', msg = msgLogin) 

@app.route('/logout', methods=['POST'])
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    # Redirect to login page
    return redirect(url_for('index'))

@app.route('/edit', methods = ['POST'])
def edit():
    msgEdit = ''
    if request.method == 'POST':
        Name = request.form['Name']
        Email = request.form['Email']
        Password = request.form['Password']
        id = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE Users SET Name = %s,  Email = %s, Password = %s WHERE CodUser = %s''', (Name, Email, Password, id))
        mysql.connection.commit()
        cursor.close()
        msgEdit = 'Changes made successfully.' 
    return redirect(url_for('profile', msg=msgEdit))

app.run(debug=True)
