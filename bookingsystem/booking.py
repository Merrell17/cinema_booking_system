import werkzeug
from flask import Flask, render_template, request, url_for, Blueprint, flash, session, redirect, current_app
from bookingsystem.extensions import db
import json
import datetime
from bookingsystem.auth import login_required
from werkzeug.security import check_password_hash, generate_password_hash

bp_booking = Blueprint('booking', __name__, url_prefix='/booking', template_folder='templates/booking')


@bp_booking.route('selectcinema', methods=["GET", "POST"])
def home():
    cur = db.connection.cursor()
    cinemas = cur.execute("SELECT * FROM cinema")
    if cinemas > 0:
        cinema_details = cur.fetchall()
    else:
        cinema_details = []

    cur.execute("SELECT title,id FROM movie")
    film_titles = cur.fetchall()

    if request.method == "POST":
        try:
            cinema_id = request.form['cinemas']
        except werkzeug.exceptions.BadRequestKeyError:
            return redirect(url_for('booking.home'))
        cur.execute("SELECT name FROM cinema WHERE id=(%s)", (cinema_id,))
        results = list(cur)[0][0]
        session['cinema_name'] = results
        session['cinema_id'] = cinema_id
        cinema_name_url = ''.join(results.split()).lower()
        session['cinema_url'] = cinema_name_url

        return redirect(url_for('booking.cinema_times', name=cinema_name_url, ))

    cur.close()

    return render_template('booking/selectCinema.html', cinemaDetails=cinema_details, film_titles=film_titles)


@bp_booking.route('selectcinema/<film>')
def film_info(film):
    cur = db.connection.cursor()
    cur.execute("""SELECT * FROM movie WHERE title=(%s)""", (film,))
    details = cur.fetchone()

    cur.execute("""SELECT C.name, S.Screening_Start, S.id 
                FROM screening S JOIN movie M ON S.movie_id = M.id
                JOIN auditorium A ON S.auditorium_id = A.id
                JOIN cinema C ON A.Cinema_id = C.id
                WHERE M.title = (%s) AND S.Screening_Start > NOW()
                ORDER BY M.title, S.Screening_Start""", (film,))

    film_times = cur.fetchall()
    # Create dictionary with keys being film titles and corresponding list of screening time values
    times = {}
    for t in film_times:
        if t[0] not in times.keys():
            times[t[0]] = [(t[1].strftime('%Y-%m-%d::%H-%M'), t[2])]
        else:
            times[t[0]].append((t[1].strftime('%Y-%m-%d::%H-%M'), t[2]))

    return render_template('booking/filmInfo.html', title=film, details=details, filmTimes=times.items())


@bp_booking.route('/cinema/<name>', methods=["GET", "POST"])
def cinema_times(name):
    cur = db.connection.cursor()
    cur.execute("""SELECT M.title, S.Screening_Start, S.id 
                    FROM screening S JOIN movie M ON S.movie_id = M.id
                    JOIN auditorium A ON S.auditorium_id = A.id
                    JOIN cinema C ON A.Cinema_id = C.id
                    WHERE C.name = (%s) AND S.Screening_Start > NOW()
                    ORDER BY M.title, S.Screening_Start""", (session['cinema_name'],))

    film_times = cur.fetchall()
    # Create dictionary with keys being film titles and corresponding list of screening time values
    times = {}
    for t in film_times:
        if t[0] not in times.keys():
            times[t[0]] = [(t[1].strftime('%d/%m  %H:%M'), t[2])]
        else:
            times[t[0]].append((t[1].strftime('%d/%m  %H:%M'), t[2]))

    dt = datetime.datetime.today()
    week_dates = [dt + datetime.timedelta(days=i) for i in range(7)]
    days = []
    for day in week_dates:
        days.append(day.strftime('%d/%m'))

    return render_template('cinemabase.html', cinemaName=session['cinema_name'],
                           filmTimes=times.items(), weekDays=days)


@bp_booking.route('/<screening>', methods=["GET", "POST"])
def seat_select(screening):
    cur = db.connection.cursor()
    cur.execute("""SELECT M.title, S.Screening_Start
                    FROM screening S JOIN movie M ON S.movie_id = M.id
                    WHERE S.id = (%s)""", (screening,))
    screening_details = cur.fetchone()
    title = screening_details[0]
    time = screening_details[1].strftime('%d %B  %H:%M')
    cur.execute("""SELECT A.row_count, A.column_count, A.id
                    FROM auditorium A JOIN screening S on S.auditorium_id = A.id
                    WHERE S.id = (%s)""", (screening,))
    screen_no = cur.fetchone()
    row = screen_no[0]
    column = screen_no[1]
    auditoriumID = screen_no[2]

    cur.execute("""     SELECT seat_id
                        FROM seat_reserved SR JOIN screening SCR on SR.screening_id=SCR.id 
                        WHERE SCR.id = (%s)""", (screening,))
    res = cur.fetchall()
    reserved_ids = [x[0] for x in res]

    reserved_numbers = []
    for s in reserved_ids:
        cur.execute("""SELECT `number`
                            FROM seat JOIN screening 
                            WHERE seat.id = (%s) AND screening.id=(%s)""", (s, screening))
        reserved_numbers.append(cur.fetchone()[0])

    if request.method=='POST':

        ticket_value = request.form.get('hidden-ticket-value')
        ticket_value = str(ticket_value)
        seats = ticket_value.split(",")
        session['seats'] = seats
        return redirect(url_for('booking.process_ticket', screening=screening, auditorium=auditoriumID,))

    return render_template('booking/seatSelect.html', screeningId=screening,
                           title=title, time=time, rows=row, columns=column,
                           auditorium=auditoriumID, reserved_numbers=reserved_numbers)


@bp_booking.route('/processticket/<auditorium>/<screening>/', methods=['GET', 'POST'])
@login_required
def process_ticket(screening, auditorium):
    cur = db.connection.cursor()
    # Get seat ID's
    seat_id = []

    # Ensure that user has gone through select_seats and hasn't just entered the URL for the page
    try:
        for seatNum in session['seats']:
            cur.execute("""SELECT s.id
                            FROM seat s JOIN auditorium A on s.auditorium_id = A.id
                            WHERE A.id = (%s) AND s.number = (%s)""", (auditorium, seatNum))
            seat = cur.fetchone()
            seat_id.append(seat[0])
    # Redirect invalid means of reaching the page
    except (KeyError, TypeError) as e:
        return redirect(url_for('booking.home'))


    cur.execute("""SELECT M.title, S.screening_start
                    FROM movie M JOIN screening S on S.movie_id=M.id
                    WHERE S.movie_id=(SELECT movie_id
                    FROM screening S 
                    WHERE S.id=(%s))""", (screening,))
    query = cur.fetchone()

    if query is None:
        return (redirect(url_for('booking.home')))

    title = query[0]
    datetime = query[1]
    date = datetime.strftime('%d %B')
    # Remove seconds
    time = datetime.strftime('%X')[:-3]
    total = format(len(session['seats']) * 9.60, '.2f')
    # Get name
    cur.execute("""SELECT first_name, last_name 
                    FROM `user` 
                    WHERE id=(%s)""", (session['user_id'], ))
    query = cur.fetchone()
    fname = query[0]
    lname = query[1]

    if request.method == "POST":

        if 'expiration' in request.form:

            expiration_date = request.form['expiration']
            card_number = request.form['card_number']


            expiration_date = '2021-11-11'
            card_number = '0000343434341323'
            card_type = 'visa'

            cur.execute("INSERT INTO payment(user_id, card_number, card_type, expiration_date) "
                    "VALUES(%s, %s, %s, %s)", (session['user_id'], card_number, card_type, expiration_date))
            db.connection.commit()

            cur.execute("SELECT max(id) FROM payment WHERE user_id = (%s)", (session['user_id'],))
            payment = cur.fetchone()[0]

            cur.execute("INSERT INTO reservation(screening_id, reserved, paid, active, user_id, payment_id) "
                    "VALUES(%s, %s, %s, %s, %s, %s)",
                    (screening, True, True, True, session['user_id'], payment))
            db.connection.commit()

            cur.execute("SELECT max(id) FROM reservation WHERE user_id = (%s)", (session['user_id'],))
            reservation = cur.fetchone()[0]

            for seat in seat_id:
                cur.execute("INSERT INTO seat_reserved(seat_id, screening_id, reservation_id) "
                        "VALUES(%s, %s, %s)", (seat, screening, reservation))
                db.connection.commit()

            cur.close()

            return redirect(url_for('booking.confirmed', user=session['user_id'], reservation=reservation))

    return render_template("booking/finaliseBooking.html", seats=session['seats'], seatid=seat_id,
                         film_title=title, total=total, date=date, time=time,
                           fname=fname, lname=lname)


### x for x, last query redundant?
# Check this is the users account?
@bp_booking.route('/confirmation/<user>/<reservation>', methods=['GET', 'POST'])
@login_required
def confirmed(user, reservation):
    cur = db.connection.cursor()

    cur.execute("""SELECT S.number
                    FROM seat S JOIN seat_reserved SR ON SR.seat_id=S.id
                    WHERE SR.reservation_id=(%s)""", (reservation,))
    seats = [x[0] for x in cur.fetchall()]

    cur.execute("""SELECT first_name, last_name
                    FROM `user` 
                    WHERE id = (%s)""", ((session['user_id']),))
    name = cur.fetchone()
    fname = name[0]
    lname = name[1]

    # Get movie's title
    cur.execute("""SELECT M.title, S.id, S.screening_start
                    FROM reservation R JOIN screening S on R.screening_id = S.id
                    JOIN movie M on M.id=S.movie_id
                    WHERE R.id=(%s);""", (reservation,))
    query = cur.fetchone()
    movie_title = query[0]
    screening = query[1]
    datetime = query[2]
    date = datetime.strftime('%d %B')

    time = datetime.strftime('%X')[:-3]

    return render_template("booking/confirmation.html", user=user, reservation=reservation,
                           seats=seats, title=movie_title, fname=fname, lname=lname, date=date, time=time)


@bp_booking.route('/expiredconfirmation/<user>/<reservation>', methods=['GET', 'POST'])
@login_required
def expired_confirmed(user, reservation):
    cur = db.connection.cursor()
    cur.execute("""SELECT first_name, last_name
                        FROM `user` 
                        WHERE id = (%s)""", ((session['user_id']),))
    name = cur.fetchone()
    fname = name[0]
    lname = name[1]

    cur.execute("""SELECT movie_title, screening_start, seat_count
                    FROM booking_data
                    WHERE id=(%s)""", (reservation,))
    query = cur.fetchone()
    title = query[0]
    datetime = query[1]
    seat_count = query[2]
    date = datetime.strftime('%d %B')
    # Remove seconds
    time = datetime.strftime('%X')[:-3]

    return render_template("booking/confirmation.html", user=user, reservation=reservation,
                           seat_count=seat_count, title=title, fname=fname, lname=lname, date=date, time=time)


# Correct film title and time but wrong ID tied to it.
@bp_booking.route('myaccount')
@login_required
def my_account():
    cur = db.connection.cursor()
    cur.execute("""SELECT id
                    FROM reservation 
                    WHERE user_id=(%s)""", (session['user_id'],))
    reservations_ids = cur.fetchall()

    user_reservations = []
    for reservation_id in reservations_ids:
        # Get
        cur.execute("""SELECT M.title, S.screening_start, R.id
                        FROM reservation R
                        JOIN screening S on R.screening_id=S.id
                        JOIN movie M on S.movie_id=M.id
                        WHERE R.id=(%s);
                            """, (reservation_id,))
        reservation = cur.fetchone()

        # Title, Time, ID
        reservation_ = (reservation[0], reservation[1].strftime('%d-%m-%Y  %H:%M'), reservation[2])
        user_reservations.append(reservation_)

    # Get bookings where the admin has deleted the main data source
    cur.execute("""SELECT movie_title, screening_start, id FROM booking_data
                    WHERE user_id=(%s)""", (session['user_id'],))

    booking_data = cur.fetchall()
    old_reservations = []
    for i in range(len(booking_data)):
        old_reservations.append(
            (booking_data[i][0], booking_data[i][1].strftime('%d-%m-%Y  %H:%M'), booking_data[i][2]))

    return render_template('booking/myAccount.html', reservations=user_reservations, old_reservations=old_reservations)


@bp_booking.route('myaccount/editdetails', methods=['GET', 'POST'])
@login_required
def edit_details():
    cur = db.connection.cursor()
    cur.execute("""SELECT *
                        FROM user
                        WHERE id=(%s)""", (session['user_id'],))
    user_details = cur.fetchone()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        cur = db.connection.cursor()
        error = None

        if not username:
            error = 'Username is required'
        elif not email:
            error = 'Email is required'
        elif not fname or not lname:
            error = 'Name is required'

        if error is None:
            cur.execute("""UPDATE `user`
                            SET username=(%s),email=(%s), first_name=(%s),last_name=(%s)
                            WHERE id=(%s)""", (username, email, fname, lname, session['user_id']))
            db.connection.commit()
            flash("Your details have been updated", "info")
            return redirect(url_for('booking.my_account'))
        flash(error)

    return render_template('booking/editDetails.html', username=user_details[1], password=user_details[2],
                           email=user_details[3], fname=user_details[4], lname=user_details[5])


@bp_booking.route('myaccount/changepassword', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['currentPassword']
        new_password = request.form['newPassword']
        confirm_password = request.form['confirmPassword']
        cur = db.connection.cursor()
        error = None
        cur.execute('SELECT * FROM `user` WHERE id = (%s)', (session['user_id'],))
        user = cur.fetchone()

        if user is None:
            error = 'There was an error fetching your account'
        elif not check_password_hash(user[2], current_password):
            error = 'The entered password is incorrect'
        elif not new_password == confirm_password:
            error = 'Your new passwords do not match'

        if error is None:
            cur.execute("""UPDATE `user`
                            SET password=(%s)
                            WHERE id=(%s)""", (generate_password_hash(new_password), session['user_id']))
            db.connection.commit()
            flash("Your password has been updated", "info")
            return redirect(url_for('booking.my_account'))

        flash(error)

    return render_template('booking/changePassword.html')
