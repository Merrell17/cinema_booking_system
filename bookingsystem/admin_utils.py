from flask import Flask, render_template, request, url_for, Blueprint
from flask_mysqldb import MySQL
from flask_admin import Admin

from bookingsystem.extensions import db

bp_admin = Blueprint('admin_utils', __name__, url_prefix='/adminutils', template_folder='templates/adminutils')

address_cinema_id = 7


@bp_admin.route('addcinema', methods=['GET', 'POST'])
def add_cinema():
    if request.method == "POST":
        address_details = request.form
        cinema_name = address_details['name']
        address1 = address_details['address1']
        address2 = address_details['address2']
        city = address_details['city']
        county = address_details['county']
        postcode = address_details['postcode']
        global address_cinema_id
        cur = db.connection.cursor()

        cur.execute("INSERT INTO address(id,address1, address2, city, county, postcode) "
                    "VALUES(%s,%s, %s, %s, %s, %s)", (address_cinema_id, address1, address2, city, county, postcode))

        cur.execute("INSERT INTO cinema(id,address_id,name) "
                    "VALUES(%s, %s, %s)", (address_cinema_id, address_cinema_id, cinema_name))

        db.connection.commit()
        cur.close()
        address_cinema_id += 1
        return "success"
    return render_template('adminutils/addCinema.html')


@bp_admin.route('selectcinema', methods=["GET", "POST"])
def home():
    cur = db.connection.cursor()
    cinemas = cur.execute("SELECT * FROM cinema")
    if cinemas > 0:
        cinema_details = cur.fetchall()
    else:
        cinema_details = []

    return render_template('adminutils/selectCinema.html', cinemaDetails=cinema_details)



@bp_admin.route('addscreens', methods=['GET', 'POST'])
def add_screen():
    cur = db.connection.cursor()
    cinemas = cur.execute("SELECT * FROM cinema")
    if cinemas > 0:
        cinema_details = cur.fetchall()
    else:
        cinema_details = []

    if request.method == "POST":
        screen_details = request.form
        screen_name = screen_details['name']
        row_count = screen_details['row_count']
        column_count = screen_details['column_count']
        cinema_name = screen_details['cinemas']

        cur.execute("INSERT INTO auditorium(screen_name, cinema_id, row_count, column_count) "
                    "VALUES(%s, %s, %s, %s)", (screen_name, cinema_name, row_count, column_count))

        db.connection.commit()
        cur.close()

    return render_template('adminutils/addScreens.html', cinemaDetails=cinema_details,)


@bp_admin.route('addfilm', methods=['GET', 'POST'])
def add_film():
    if request.method == "POST":
        cur = db.connection.cursor()
        film_details = request.form
        title = film_details['title']
        director = film_details['director']
        description = film_details['description']
        duration = film_details['duration']

        cur.execute("INSERT INTO movie(title, director, description, duration_min) "
                    "VALUES(%s, %s, %s, %s)", (title, director, description, duration))

        db.connection.commit()
        cur.close()
    return render_template('adminutils/addFilm.html')


@bp_admin.route('createscreening', methods=['GET', 'POST'])
def create_screening():

    cur = db.connection.cursor()
    films = cur.execute("SELECT * FROM movie")
    if films > 0:
        film_details = cur.fetchall()
    else:
        film_details = []

    auditorium_details = cur.execute('SELECT auditorium.id, name, screen_name FROM Auditorium '
                                     'INNER JOIN Cinema ON auditorium.cinema_id = cinema.id')
    auditorium_details = cur.fetchall()

    if request.method == "POST":
        cur = db.connection.cursor()
        screening_details = request.form
        screen_id = screening_details['screen']
        film_id = screening_details['films']
        start_time = screening_details['film_time']

        cur.execute("INSERT INTO screening(movie_id, auditorium_id, screening_start) "
                    "VALUES(%s, %s, %s)", (film_id, screen_id, start_time))
        db.connection.commit()
        cur.close()



    return render_template('createScreening.html',filmDetails=film_details,
                           auditoriumDetails=auditorium_details)
