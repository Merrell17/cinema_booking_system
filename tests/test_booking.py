import pytest
from bookingsystem.extensions import db

import datetime

global expected_cinema_id

# Autouse functions are automatically invoked for each test function defined in
# the same module. We can use it act as an admin, setting up a cinema, screen,
# film and screening. The yield keyword is where each test in this module is run.
# The code after yield will be run after each test. Here we can teardown what we
# have created prior.
@pytest.fixture(autouse=True)
def test_set_up_film_screening(client, auth, app):
    auth.login(username='admin', password='1234')
    assert client.get('/adminutils/addcinema').status_code == 200
    client.post('/adminutils/addcinema', data={'name': 'Testing Booking', 'address1': '1', 'address2': '2',
                                                   'city': 'Test', 'county': 'Test ', 'postcode': 'Test'})
    client.post('/adminutils/addfilm',
                data={'imdb_id': '', 'title': 'TestTitle', 'director': 'Test Booking Director',
                      'description': 'Test Booking Description',
                      'duration': '100', 'movie_image': ''})
    with app.app_context():
        # Get the inserted cinemas ID
        cur = db.connection.cursor()
        cur.execute("""SELECT MAX(id) FROM cinema""")
        # Allow the cinema id to be used in tests
        global expected_cinema_id
        expected_cinema_id = cur.fetchone()[0]
        cur.execute("""SELECT id FROM cinema WHERE `name`='Testing Booking' """)
        retrieved_cinema_id = cur.fetchone()[0]
        assert expected_cinema_id == retrieved_cinema_id

        # Get the inserted film ID
        cur.execute("""SELECT MAX(id) FROM `movie`""")
        expected_film_id = cur.fetchone()[0]
        cur.execute("""SELECT id FROM movie WHERE `title`='TestTitle' """)
        retrieved_film_id = cur.fetchone()[0]
        assert expected_film_id == retrieved_film_id
        cur.close()

    client.post('/adminutils/addscreens', data={'name': '1', 'row_count': '10', 'column_count': '10',
                                                'cinemas': retrieved_cinema_id})
    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT id FROM auditorium WHERE cinema_id=(%s)""", (retrieved_cinema_id,))
        screen_id = cur.fetchone()[0]
        cur.close()

    # Set the timing for the screening 3 days from now at 15:35pm
    today = datetime.datetime.today()
    date = today + datetime.timedelta(days=3)
    date = date.strftime('%Y-%m-%d')+'T15:35'
    client.post('/adminutils/createscreening', data={'screen': screen_id, 'films': retrieved_film_id,
                                                    'film_time': date, })
    # Logout of admin account and run tests
    auth.logout()
    yield

    # Teardown data
    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""DELETE FROM `movie` WHERE id=(%s)""", (retrieved_film_id,))
        cur.execute("""DELETE FROM `cinema` WHERE id=(%s)""", (retrieved_cinema_id,))
        cur.execute("""DELETE FROM `screening` WHERE auditorium_id=(%s)""", (screen_id,))
        db.connection.commit()
        cur.close()


def test_edit_details(client, app, auth):
    auth.login(username='admin', password='1234')
    assert client.get('booking/myaccount/editdetails').status_code == 200

    response = client.get('booking/myaccount/editdetails')
    assert b"admin" in response.data

    # Change several things, e.g admin -> admin10
    response = client.post('booking/myaccount/editdetails', data={'username': 'admin10', 'email': 'new_email@example.com',
                                                                  'fname': 'firsttest', 'lname': 'lasttest'})
    # Check that admin details have changed
    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT * FROM user WHERE username='admin10'""")
        admin_user_row = cur.fetchone()
        assert admin_user_row[1] == 'admin10'

    # Reset admin details
    client.post('booking/myaccount/editdetails', data={'username': 'admin', 'email': 'new_example@gmail.com',
                                                    'fname': 'John', 'lname': 'Doe'})
    auth.logout()


@pytest.mark.run(order=1)
def test_index(client, auth):
    response = client.get('http://127.0.0.1:5000/booking/selectcinema')
    # Log in and register should be visible on the nav bar when not not logged in
    assert b"Log In" in response.data
    assert b"Register" in response.data
    assert b"Log Out" not in response.data
    # Login and check we can now logout
    auth.login()
    response = client.get('http://127.0.0.1:5000/booking/selectcinema')
    assert b'Log Out' in response.data


def test_select_cinema(client):
    # Select the cinema we created in the test setup
    response = client.post('http://127.0.0.1:5000/booking/selectcinema', data={'cinemas': expected_cinema_id})
    # Check we are being redirected here
    assert response.headers['Location'] == "http://127.0.0.1:5000/booking/cinema/Testing%20Booking/0"


# Ensure that when trying to access a URL that requires login, we get redirected to login
def test_login_required(client):
    response = client.post('/booking/processticket/40/80/')
    assert response.headers['Location'] == 'http://localhost/auth/login'

# Here we are selecting a film on the homepage, not a cinema, so look for the details we added
def test_film_info_page(client):
    response = client.get('booking/selectcinema/TestTitle')
    # Ensure relevant Info is being displayed
    assert b"Test Booking Director" in response.data
    assert b"Duration: 100 Minutes" in response.data

    # Ensure there is a link to the test cinema, where we created a screening for the film
    assert b"Testing Booking" in response.data


def test_cinema_home_page(client):
    # Go to cinema homepage, with the current week(0) selected
    response = client.get('booking/cinema/Testing%20Booking/0')
    # We created a screening in 3 days time in setup, at 15:35pm so the screening should be here
    assert b"TestTitle" in response.data
    assert b"15:35" in response.data


# Generally want smaller unit tests but given that there is a chain of operations required in order to make a booking
# this test is longer. We use assert statements throughout so we can locate any issues.
def test_full_booking_process(client, app, auth):
    # Get the necessary ID's for the screening created in set_up_film_screening()
    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT id FROM movie WHERE `title`='TestTitle' """)
        film_id = cur.fetchone()[0]
        cur.execute("""SELECT * FROM SCREENING WHERE movie_id=(%s)""", (film_id,))
        film_screening = cur.fetchone()
        screening_id = film_screening[0]
        screen_id = film_screening[2]
        cur.execute("""SELECT id FROM user WHERE username='admin' """)
        account = cur.fetchone()
        admin_id = account[0]
    # Check the select seat url exists for the created screening
    seat_map_url = 'booking/' + str(screening_id)
    assert client.get(seat_map_url).status_code == 200
    response = client.get(seat_map_url)
    # Check the seat map contains info about the screening
    assert b"TestTitle" in response.data
    assert b"15:35" in response.data

    # Login required to select and book seats, we'll use the admin account
    auth.login(username='admin', password='1234')

    # Select seats on seat map page (seats 1, 2 and 3) and submit
    response = client.post(seat_map_url, data={'hidden-ticket-value': '0,1,2'})

    # Check that we have been rerouted to the process payment url after selecting seats
    process_ticket_url = 'booking/processticket/{screen}/{screening}/'
    assert (process_ticket_url.format(screen=screen_id, screening=screening_id)) in response.headers['Location']

    # Enter card details into the payment form, creating a booking
    process_payment_url = response.headers['Location']
    response = client.post(process_payment_url, data={'expiration': '01/01', 'card_number': '0000000000000'})


    # Use database cursor to check that our bookings have been created, 1 booking with 3 seats selected
    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT * FROM reservation WHERE screening_id=(%s)""", (screening_id,))
        bookings = cur.fetchall()
        reservation_id = bookings[0][0]
        cur.execute("""SELECT * FROM seat_reserved WHERE screening_id=(%s)""", (screening_id,))
        reserved_seats = cur.fetchall()
        assert len(bookings) == 1
        assert len(reserved_seats) == 3
    # Finally we will check that the booking confirmation is present on our My Account page
    confirmation_url = ('http://localhost/booking/confirmation/{}/{}'.format(admin_id, reservation_id))
    assert client.get(confirmation_url).status_code == 200
    response = client.get('booking/myaccount')
    assert b"TestTitle:" in response.data


# Change password to 123, logout, log back in and check our user session variable is set (we are logged in)
def change_password(client, auth, app):
    auth.login(username='admin', password='1234')
    client.post('booking/myaccount/changepassword', data={'currentPassword': '1234', 'newPassword': '123',
                                                        'confirmPassword': '123'})
    auth.logout()
    auth.login(username='admin', password='123')
    assert app.session['user_id'] is not None