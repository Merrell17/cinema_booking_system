import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import re
from flask_mysqldb import MySQL
from bookingsystem.extensions import db
import random
import string

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


@bp_auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        cur = db.connection.cursor()
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required'
        elif not fname or not lname:
            error = 'Full name is required'

        cur.execute('SELECT id FROM user WHERE username = (%s)', (username,))
        if cur.fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        cur.execute('SELECT email FROM user WHERE email = (%s)', (email,))
        if cur.fetchone() is not None:
            error = 'Email {} is already taken.'.format(email)

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            error = 'Email entered is not of a valid format'

        if error is None:

            cur.execute(
                "INSERT INTO user(username, password, email, first_name, last_name, is_admin)"
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (username, generate_password_hash(password), email, fname, lname, 0))
            db.connection.commit()

            cur.close()
            flash('Account created!')
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp_auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = db.connection.cursor()
        error = None
        cur.execute('SELECT * FROM user WHERE username = (%s)', (username,))
        user = cur.fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user[2], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('booking.home'))

        flash(error)

    return render_template('auth/login.html')


@bp_auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    cur = db.connection.cursor()
    if user_id is None:
        g.user = None
    else:
        cur.execute(
            'SELECT * FROM user WHERE id = (%s)', (user_id,)
        )
        g.user = cur.fetchone()
        # Store whether use is admin
        try:
            is_admin = g.user[6]
            g.admin = bool(is_admin)
        except:
            g.admin = False


@bp_auth.route('/logout')
def logout():
    # Clear session variables so user doesn't have selected cinema or my account
    session.clear()
    flash("You have been logged out")
    return redirect(url_for('auth.login'))


def check_admin(admin_required_page):
    @functools.wraps(admin_required_page)
    def wrapper(**kwargs):
        # Check g for login before database search
        if g.user is None:
            flash('Login as an admin to access this page')
            return redirect(url_for('auth.login'))

        # Pull user details check if they're an admin
        cur = db.connection.cursor()
        cur.execute('SELECT is_admin FROM user WHERE id = (%s)', (session['user_id'],))
        is_admin = cur.fetchone()[0]

        if not is_admin:
            flash("Your account does not have the privileges required to view to this page")
            return redirect(url_for('auth.login'))

        return admin_required_page(**kwargs)

    return wrapper


# View wrapper used to stop users accessing login required pages
def check_login(login_required_page):
    @functools.wraps(login_required_page)
    def wrapper(**kwargs):
        # Check g variable which is set when users login, if none redirect
        if g.user is None:
            flash("You must be logged in to access this page")
            return redirect(url_for('auth.login'))

        return login_required_page(**kwargs)

    return wrapper





# A view to generate admin accounts for testing purposes
@bp_auth.route('/createadmin', methods=('GET', 'POST'))
def create_admin():

    letters = string.ascii_lowercase
    usern = (''.join(random.choice(letters) for i in range(5)))
    passw = (''.join(random.choice(letters) for i in range(3)))
    email = usern + '@mail.com'

    cur = db.connection.cursor()
    cur.execute('SELECT id FROM user WHERE username = (%s)', (usern,))

    # Ensure that randomly generated details don't cause issues
    error = None
    if cur.fetchone() is not None:
        error = 'User {} is already registered.'.format(usern)

    cur.execute('SELECT email FROM user WHERE email = (%s)', (email,))
    if cur.fetchone() is not None:
        error = 'Email {} is already taken.'.format(email)

    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        error = 'Email entered is not of a valid format'

    if error is None:
        cur.execute(
            "INSERT INTO user(username, password, email, first_name, last_name, is_admin)"
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (usern, generate_password_hash(passw), email, 'John', 'Doe', 1))
        db.connection.commit()

    return render_template('auth/generateAdmin.html', usern=usern, passw=passw, email=email)
