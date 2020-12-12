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
        cur = db.connect.cursor()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif cur.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            cur.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp_auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    cur = db.connect.cursor()
    if user_id is None:
        g.user = None
    else:
        g.user = cur.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp_auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))