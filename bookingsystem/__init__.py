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

address_cinema_id = 6


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
        address_cinema_id += 6
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

    if request.method == "POST":
        screen_details = request.form
        screen_name = screen_details['name']
        row_count = screen_details['row_count']
        column_count = screen_details['column_count']
        cinema_name = screen_details['cinemas']


        cinema_id = cur.execute("SELECT id FROM Cinema WHERE name IS %s", [cinema_name])


        cur.execute("INSERT INTO auditorium(screen_name, cinema_id, row_count, column_count) "
                    "VALUES(%s, %s, %s, %s)", (screen_name, cinema_id, row_count, column_count))

    return render_template('addScreens.html', cinemaDetails=cinema_details)


if __name__ == '__main__':
    app.run(debug=True)
