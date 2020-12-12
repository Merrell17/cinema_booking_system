import os

from flask import Flask
from flask_mysqldb import MySQL
from flask_admin import Admin
from bookingsystem import auth, admin_utils

from bookingsystem.extensions import db


def create_app():

    app = Flask(__name__)
    admin = Admin(app, name='microblog', template_mode='bootstrap3')

    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '1234'
    app.config['MYSQL_DB'] = 'flaskapp'
    app.config['MYSQL_HOST'] = 'localhost'
    db.init_app(app)

    app.register_blueprint(auth.bp_auth)
    app.register_blueprint(admin_utils.bp_admin)

    return app
