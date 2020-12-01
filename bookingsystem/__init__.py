import os

from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)

address_cinema_id = 7


@app.route('/addcinema', methods=['GET', 'POST'])
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
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO address(id,address1, address2, city, county, postcode) "
                    "VALUES(%s,%s, %s, %s, %s, %s)", (address_cinema_id, address1, address2, city, county, postcode))
        
        cur.execute("INSERT INTO cinema(id,address_id,name) "
                    "VALUES(%s, %s, %s)", (address_cinema_id, address_cinema_id, cinema_name))

        mysql.connection.commit()
        cur.close()
        address_cinema_id += 1
        return "success"
    return render_template('addCinema.html')


@app.route('/selectcinema', methods = ["GET", "POST"])
def home():
    cur = mysql.connection.cursor()
    cinemas = cur.execute("SELECT * FROM cinema")
    if cinemas > 0:
        cinema_details = cur.fetchall()
    else:
        cinema_details = []

    return render_template('selectCinema.html', cinemaDetails=cinema_details)



@app.route('/addscreens', methods=['GET', 'POST'])
def add_screen():
    cur = mysql.connection.cursor()
    cinemas = cur.execute("SELECT * FROM cinema")
    if cinemas > 0:
        cinema_details = cur.fetchall()
    else:
        cinema_details = []

    films = cur.execute("SELECT * FROM movie")
    if films > 0:
        film_details = cur.fetchall()
    else:
        film_details = []

    if request.method == "POST":
        screen_details = request.form
        screen_name = screen_details['name']
        row_count = screen_details['row_count']
        column_count = screen_details['column_count']
        cinema_name = screen_details['cinemas']

        cur.execute("INSERT INTO auditorium(screen_name, cinema_id, row_count, column_count) "
                    "VALUES(%s, %s, %s, %s)", (screen_name, cinema_name, row_count, column_count))

        mysql.connection.commit()
        cur.close()

    return render_template('addScreens.html', cinemaDetails=cinema_details,)


@app.route('/addfilm', methods=['GET', 'POST'])
def add_film():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        film_details = request.form
        title = film_details['title']
        director = film_details['director']
        description = film_details['description']
        duration = film_details['duration']

        cur.execute("INSERT INTO movie(title, director, description, duration_min) "
                    "VALUES(%s, %s, %s, %s)", (title, director, description, duration))

        mysql.connection.commit()
        cur.close()
    return render_template('addFilm.html')

@app.route('/createscreening', methods=['GET', 'POST'])
def create_screening():
    cur = mysql.connection.cursor()
    cinemas = cur.execute("SELECT * FROM cinema")
    if cinemas > 0:
        cinema_details = cur.fetchall()
    else:
        cinema_details = []

    films = cur.execute("SELECT * FROM movie")
    if films > 0:
        film_details = cur.fetchall()
    else:
        film_details = []

    return render_template('createScreening.html', cinemaDetails=cinema_details, filmDetails=film_details)


if __name__ == '__main__':
    app.run(debug=True)
