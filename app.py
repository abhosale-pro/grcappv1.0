# importing rendering template for html files, request parameters
from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
# from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

# initialising the app
app = Flask(__name__)

# dev or production enviroment

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Smart$2025'
app.config['MYSQL_DB'] = 'grcapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)


# Routing in FLASK


# function to render Home template
@app.route('/')
def index():
    return render_template('Home.html')

# function to render Login template


@app.route('/loginPage')
def loginPage():
    return render_template('loginPage.html')

# function to render Home template


@app.route('/gov-dcf')
def govdcf():
    return render_template('gov-dcf.html')


@app.route('/gov-dcf-controls')
def govdcfcontrols():
    return render_template('/gov-dcf-controls.html')


@app.route('/gov-dp')
def govdp():
    return render_template('gov-dp.html')


@app.route('/gov-de')
def govde():
    return render_template('gov-de.html')


@app.route('/rm-sr')
def rmsr():
    return render_template('rm-sr.html')


@app.route('/am-ma')
def amma():
    return render_template('am-ma.html')


@app.route('/assess-pcidss')
def assesspcidss():
    return render_template('assess-pcidss.html')


# signup form

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = StringField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                    (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')
    return render_template('register.html', form=form)

# User login


@app.route('/loginPage', methods=['GET', 'POST'])
def loginpage():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute(
            "SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):

                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return render_template('Home.html')
            else:
                error = 'Invalid login'
                return render_template('loginPage.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('loginPage.html', error=error)


# Check if user logged in


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('loginPage'))
    return wrap

# Logout


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('loginPage'))


# checking if app is running
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()
