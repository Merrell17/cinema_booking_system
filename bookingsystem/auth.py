import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flask_mysqldb import MySQL
from bookingsystem.extensions import db

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


@bp_auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        cur = db.connection.cursor()
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
            error = 'Email {} is already taken.'.format(username)

        if error is None:

            cur.execute(
                "INSERT INTO user(username, password, email, first_name, last_name, is_admin)"
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (username, generate_password_hash(password), email, fname, lname, 0))
            db.connection.commit()

            cur.close()
            flash('Account created!')
            return redirect(url_for('auth.login'))

        db.connection.commit()  #tab in?
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
        is_admin = g.user[6]
        g.admin = bool(is_admin)


@bp_auth.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Login as an admin to access this page')
            return redirect(url_for('auth.login'))

        cur = db.connection.cursor()
        cur.execute('SELECT is_admin FROM user WHERE id = (%s)', (session['user_id'],))
        is_admin = cur.fetchone()[0]

        if not is_admin:
            flash("Login as an administrator to access this page")
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
