import os

from flask import Flask, g
from flask_mysqldb import MySQL
from flask_admin import Admin
from bookingsystem import auth, admin_utils, booking

from bookingsystem.extensions import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    app.config['SECRET_KEY'] = 'key'

    # Local user: 'root'
    # Pythonanywhere user: 'Merrell17'
    app.config['MYSQL_USER'] = 'Merrell17'

    # Pythonanywhere pwd: 'root1234'
    # AWS pwd: '12345678'
    # Local pwd: '1234'
    app.config['MYSQL_PASSWORD'] = 'root1234'

    # Pythonanywhere dbname = 'Merrell17$flaskapp'
    # Local dbname: = 'flaskapp'
    app.config['MYSQL_DB'] = 'Merrell17$flaskapp'

    # AWS host: 'awsflaskbooking.cicsvmdk9o8l.eu-west-2.rds.amazonaws.com'
    # Pythonanywhere host: 'Merrell17.mysql.pythonanywhere-services.com'
    # Local host : 'localhost'
    app.config['MYSQL_HOST'] = 'Merrell17.mysql.pythonanywhere-services.com'

    root_folder = os.path.dirname(os.path.abspath(__file__))
    images = os.path.join('static', 'imgs')
    app.config['IMAGE_UPLOADS'] = os.path.join(root_folder, images)

    # app.config['IMAGE_UPLOADS'] = os.path.abspath("C:/Users/Hugh/PycharmProjects/New folder/cinema_booking_system/bookingsystem/static/imgs")

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
