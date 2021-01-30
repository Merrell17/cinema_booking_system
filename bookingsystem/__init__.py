import os

from flask import Flask
from flask_mysqldb import MySQL
from flask_admin import Admin
from bookingsystem import auth, admin_utils, booking

from bookingsystem.extensions import db

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    app.config['SECRET_KEY'] = 'key'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '1234'
    app.config['MYSQL_DB'] = 'flaskapp'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['IMAGE_UPLOADS'] = os.path.abspath("C:/Users/Hugh/PycharmProjects/New folder/cinema_booking_system/bookingsystem/static/imgs")

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

        # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp_auth)
    app.register_blueprint(admin_utils.bp_admin)
    app.register_blueprint(booking.bp_booking)
    app.debug = True
    return app
