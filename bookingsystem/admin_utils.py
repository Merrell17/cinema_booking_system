from flask import Flask, render_template, request, url_for, Blueprint, flash, session, redirect, current_app
from flask_mysqldb import MySQL
from flask_admin import Admin
import os
import imdb
import datetime
from bookingsystem.extensions import db

from bookingsystem.auth import admin_required

bp_admin = Blueprint('admin_utils', __name__, url_prefix='/adminutils', template_folder='templates/adminutils')

address_cinema_id = 25

# Add Cinema to database
@bp_admin.route('addcinema', methods=['GET', 'POST'])
@admin_required
def add_cinema():
    # Get form details
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

        # Check for errors
        error = None
        if not cinema_name:
            error = 'title is required.'

        cur.execute('SELECT `name` FROM cinema WHERE name = (%s)', (cinema_name,))
        if cur.fetchone() is not None:
            error = 'There is already a cinema called {}'.format(cinema_name)

        # Insert Cinema into database
        if error is None:
            cur.execute("INSERT INTO address(id,address1, address2, city, county, postcode) "
                        "VALUES(%s,%s, %s, %s, %s, %s)", (address_cinema_id, address1, address2, city, county, postcode))

            cur.execute("INSERT INTO cinema(id,address_id,name) "
                        "VALUES(%s, %s, %s)", (address_cinema_id, address_cinema_id, cinema_name))

            db.connection.commit()
            cur.close()
            address_cinema_id += 1
            flash("Success")
        else:
            flash(error)

    return render_template('adminutils/addCinema.html')


@bp_admin.route('addscreens', methods=['GET', 'POST'])
@admin_required
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

        error = None

        if not screen_name:
            error = 'screen name is required.'
        elif not cinema_name:
            error = 'cinema_name is required'
        elif not column_count or int(column_count) < 1:
            error = 'Invalid number of columns'
        elif not row_count or int(row_count) < 1:
            error = 'Invalid number of rows'

        cur.execute("""SELECT screen_name 
                        FROM auditorium
                        WHERE cinema_id = (%s)
                        AND screen_name = (%s)""", ((cinema_name), (screen_name)))
        if cur.fetchone() is not None:
            error = 'There is already a screen number {} for this cinema'.format(screen_name)

        if error is None:
            cur.execute("INSERT INTO auditorium(screen_name, cinema_id, row_count, column_count) "
                            "VALUES(%s, %s, %s, %s)", (screen_name, cinema_name, row_count, column_count))
            db.connection.commit()
            cur.execute("SELECT max(id) FROM auditorium")
            screen_id = cur.fetchone()[0]

            for i in range(int(column_count) * (int(row_count))):
                cur.execute("INSERT INTO seat(`number`, auditorium_id) "
                            "VALUES(%s, %s)", (i, screen_id))
        
            db.connection.commit()
            cur.close()

        flash(error)

    return render_template('adminutils/addScreens.html', cinemaDetails=cinema_details,)


@bp_admin.route('addfilm', methods=['GET', 'POST'])
@admin_required
def add_film():
    if request.method == "POST":
        # ia = imdb.IMDb()
        # a = ia.get_movie("0325980")
        # a['runtimes']
        # a['plot outline']
        #for director in a['directors']:
            #print(director['name'])

        cur = db.connection.cursor()
        imbd_id = request.form['imdb_id']
        imbd_film = None
        error = None


        if imbd_id != '':
            ia = imdb.IMDb()

            try:
                imbd_film = ia.get_movie(imbd_id)
                title = imbd_film['title']
                directors = []
                for dir in imbd_film['directors']:
                    directors.append(str(dir['name']))
                duration = imbd_film['runtimes']
                description = imbd_film['plot outline']
                director = ' '.join(directors)
            except imdb._exceptions.IMDbParserError:
                imbd_film = None
                pass

        else:
            film_details = request.form
            title = film_details['title']
            director = film_details['director']
            description = film_details['description']
            duration = film_details['duration']

        if not imbd_film:
            error = 'Invalid IMDb ID, enter details manually or try again'
        elif not title:
            error = 'title is required.'
        elif not duration:
            error = 'duration is required'

        cur.execute('SELECT title FROM movie WHERE title = (%s)', (title,))
        if cur.fetchone() is not None:
            error = 'The film {} is already available'.format(title)

        if error is None:

            cur.execute("INSERT INTO movie(title, director, description, duration_min) "
                    "VALUES(%s, %s, %s, %s)", (title, director, description, duration))

            db.connection.commit()
            cur.close()
            image = request.files['movie_image']
            image_name = title + ".jpg"

            image.save(os.path.join(current_app.config["IMAGE_UPLOADS"], image_name))
            flash('Successfully added film ' + title)
        else:
            flash(error)

    return render_template('adminutils/addFilm.html')


@bp_admin.route('createscreening', methods=['GET', 'POST'])
@admin_required
def create_screening():

    cur = db.connection.cursor()
    films = cur.execute("SELECT * FROM movie")
    if films > 0:
        film_details = cur.fetchall()
    else:
        film_details = []

    auditorium_details = cur.execute('SELECT auditorium.id, name, screen_name FROM auditorium '
                                     'INNER JOIN cinema ON auditorium.cinema_id = cinema.id')
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
        flash('Screening created!')

    return render_template('createScreening.html', filmDetails=film_details,
                           auditoriumDetails=auditorium_details)

@bp_admin.route('makedeletions', methods=['GET', 'POST'])
@admin_required
def deletions():
    # Get database items for template to delete
    cur = db.connection.cursor()

    cinemas = cur.execute("SELECT * FROM cinema")
    if cinemas > 0:
        cinema_details = cur.fetchall()
    else:
        cinema_details = []


    movies = cur.execute("SELECT id, title FROM movie")
    if movies > 0:
        movies = cur.fetchall()
    else:
        movies = []

    auditoriums = cur.execute("""SELECT A.id, A.screen_name, C.name 
                                FROM auditorium A JOIN cinema C on A.cinema_id = C.id """)
    if auditoriums > 0:
        auditoriums = cur.fetchall()
    else:
        auditoriums = []

    # Get form data and perform deletions
    if request.method == 'POST':
        # Check which form was posted
        if 'cinemas' in request.form:

            cinema_id = request.form['cinemas']
            cur.execute("""DELETE FROM cinema WHERE id=(%s)""", (cinema_id,))
            db.connection.commit()
            flash("Successfully Deleted Cinema")
            return redirect(url_for('admin_utils.deletions'))

        elif 'movies' in request.form:

            movie_id = request.form['movies']
            cur.execute("""SELECT title FROM movie WHERE id=(%s)""", (movie_id,))
            title = cur.fetchone()[0]
            movie_file = str(title) + '.jpg'
            imgs_path = "bookingsystem/static/imgs/"
            if not os.path.exists(imgs_path + movie_file):
                flash(imgs_path + movie_file + "doesnt exist")
            else:
                os.remove(imgs_path + movie_file)

            # Save necessary data for user before film and related cascades are deleted
            cur.execute(""" INSERT INTO booking_data
                            SELECT R.id, R.user_id, M.title, S.screening_start, COUNT(SR.reservation_id) AS seats
                            FROM reservation R 
                            JOIN seat_reserved SR on R.id = SR.reservation_id
                            JOIN screening S ON R.screening_id=S.id
                            JOIN movie M on S.movie_id=M.id
                            WHERE M.id=(%s)
                            GROUP BY R.user_id, R.id""", (movie_id,))

            cur.execute("""DELETE FROM movie WHERE id=(%s)""", (movie_id,))
            db.connection.commit()
            flash("Deleted Film: " + title)

        elif 'auditoriums' in request.form:
            auditorium_id = request.form['auditoriums']
            cur.execute("""DELETE FROM auditorium WHERE id=(%s)""", (auditorium_id,))
            db.connection.commit()
            flash("Successfully Deleted auditorium")
            return redirect(url_for('admin_utils.deletions'))


        return redirect(url_for('admin_utils.deletions'))



    return render_template('adminutils/makeDeletions.html', cinemaDetails=cinema_details,
                           movies=movies, auditoriums=auditoriums)
