import os

from flask import Flask, render_template, request
from flask_mysqldb import MySQL


app = Flask(__name__)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)

address_cinema_id = 3


@app.route('/', methods=['GET', 'POST'])
def hello():
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
        return 'success'
    return render_template('addCinema.html')


if __name__ == '__main__':
    app.run(debug=True)
