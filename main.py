#IMPORTING OF IMPORTANT LABRARIES FOR THE PROJECT
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import telegram
import asyncio
#from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import webview

#CREATING A FLASK APPLCATON
app = Flask(__name__)

#APP SECRET KEEP DATA INTERGRITY
app.secret_key = '123456789'

#MYSQL DATABASE CONNECTON DETAILS
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fkl25220212'
app.config['MYSQL_DB'] = 'sagebot'

#SECOND CONNECTION TO THE DATABASE
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='fkl25220212',
    database='sagebot'
)

#USED TO SETUP MYSQL SEVER FOR OUR APPLICATION
mysql = MySQL(app)

#FUCTION USED TO RENDER THE TEMPLATE FOR OUR LANDNG PAGE
@app.route('/')
def landing():
    return render_template('landing.html')

#FUCTION USED TO RENDER THE ADMIN LOGIN PAGE
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Passwords match, log the user in
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admins WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

#FUNCTION USED FOR THE ADMIN LOGOUT
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

#FUNCTION USED TO HANDLE ADMIN REGISTRATION
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    #CHECKING IF THE USE ALREADY EXIST
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admins WHERE email = %s', (email,))
        account = cursor.fetchone()
        #INPUT VALIDATION CHECKS
        if account:
            msg = 'Email already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO admins VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

#FUNCTION USED TO HANDLE ADMIN HOME PAGE
@app.route('/pythonlogin/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#FUNCTION USED TO HANDLE ADMIN PROFILE SECTION
@app.route('/pythonlogin/profile')
def profile():
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admins WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

#FUNCTION USED TO POST INFORMATION FROM ADMINS FORM
@app.route('/pythonlogin/post', methods=['GET', 'POST'])
async def post():
    if request.method == 'POST':
        unit = request.form['unit']
        instructor = request.form['instructor']
        subject = request.form['subject']
        information = request.form['information']
        date = request.form['date']
        time = request.form['time']

        telegram_message = f'Hi,Everyone,\nUpdate from {instructor},\nUnit Code: {unit}.\n Subject:{subject}\n {information} \n Best regards, \n {date} {time}'

        bot = telegram.Bot(token='6147310535:AAHdNTPRh7QKdE329g1Z6FU8g2y4f0RmdB0')

        await bot.sendMessage(chat_id=1717744928, text=telegram_message)

        return render_template('dataform.html')
    return render_template('dataform.html')



#FUNCTION USED TO RETURN THE NEWS FROM MYSQL DATABASE
def get_data():
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM news';
    cursor.execute(query)
    results = cursor.fetchall()
    return results
#RENDERING NEWS HTML TABLE
@app.route('/pythonlogin/check/', methods=['GET', 'POST'])
def check():
    data = get_data()
    return render_template('checkpost.html',data = data)

#ITERATION FUNCTION USED TO POST MESSAGES FROM THE SQL DB
@app.route('/pythonlogin/check/send', methods=['GET', 'POST'])
async def send():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM news')
    data = cursor.fetchall()
    # Create a Telegram bot instance
    bot = telegram.Bot(token='6147310535:AAHdNTPRh7QKdE329g1Z6FU8g2y4f0RmdB0')
    # Iterate over the data and send it to the Telegram bot
    for row in data:
        message = f'Hello Everyone \nUpdate for:{row[1]} \nInstructor:{row[2]}\nSubject:{row[3]}\n     Information:\n{row[4]}\nBest Regards\n   {row[5]}\n   {row[6]}'
        await bot.sendMessage(chat_id=1717744928, text=message)
        await bot.send_message(chat_id='@masenouni', text=message)
    # Redirect back to the form page
    return render_template('checkpost.html')

#FUNCTION USED TO DELETE THE MESSAGES WHICH HAVE BEEN POSTED
@app.route('/pythonlogin/delete')
def delete():
    cursor = conn.cursor()
    delete_query = 'DELETE FROM news'
    cursor.execute(delete_query)
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('checkpost.html')

#FUNCTION USED TO HANDLE INSTRUCTORS LOGIN
@app.route('/userlogin/', methods=['GET', 'POST'])
def userlogin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM instructors WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('userhome'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('userindex.html', msg=msg)

#FUNCTION USED TO RENDER THE INSTRUCTORS' HOME PAGE
@app.route('/userlogin/home')
def userhome():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('userhome.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('userlogin'))

#FUNCTION USED TO HANDLE INSTRUCTORS' LOGOUT
@app.route('/userlogin/logout')
def userlogout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('userlogin'))

#FUNCTION USED TO HANDLE INSTUCTORS' REGSTRATION
@app.route('/userlogin/register', methods=['GET', 'POST'])
def userregister():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM instructors WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Email already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO instructors VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('userregister.html', msg=msg)

#FUNCTION USED TO RENDER INSTRUCTORS PROFILE PAGE
@app.route('/userlogin/profile')
def userprofile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM instructors WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('userprofile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('userlogin'))

#FUNCTION USED TO INSERT NEW INTO THE DATABASE
@app.route('/userlogin/submit', methods = ['GET','POST'])
def submit():
    if request.method == 'POST':
        unit = request.form['unit']

        instructor = request.form['instructor']
        subject = request.form['subject']
        information = request.form['information']
        date = request.form['date']
        time = request.form['time']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO news VALUES (NULL, %s, %s, %s, %s, %s, %s)', (unit, instructor, subject,information,date,time,))
        mysql.connection.commit()
        # Show registration form with message (if any)
    return render_template('userdataform.html')

#RUNNING OUR APPLICATION
if __name__ == "__main__":
    app.run(debug=True)
    #webview.start()



