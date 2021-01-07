from flask import Flask, render_template, request, url_for, Blueprint, flash, session, redirect, current_app
from bookingsystem.extensions import db
import json
bp_booking = Blueprint('booking', __name__, url_prefix='/booking', template_folder='templates/booking')

@bp_booking.route('selectcinema', methods=["GET", "POST"])
def home():
    cur = db.connection.cursor()
    cinemas = cur.execute("SELECT * FROM cinema")
    if cinemas > 0:
        cinema_details = cur.fetchall()
    else:
        cinema_details = []
    if request.method == "POST":
        cinema_id = request.form['cinemas']
        cur.execute("SELECT name FROM cinema WHERE id=(%s)", (cinema_id,))
        results = list(cur)[0][0]
        session['cinema_name'] = results
        session['cinema_id'] = cinema_id
        cinema_name_url = ''.join(results.split()).lower()
        session['cinema_url'] = cinema_name_url

        return redirect(url_for('booking.cinema_times', name=cinema_name_url, ))

    cur.close()

    return render_template('booking/selectCinema.html', cinemaDetails=cinema_details)


@bp_booking.route('/cinema/<name>', methods=["GET", "POST"])
def cinema_times(name):
    cur = db.connection.cursor()
    cur.execute("""SELECT M.title, S.Screening_Start, S.id 
                FROM screening S JOIN movie M ON S.movie_id = M.id
                JOIN auditorium A ON S.auditorium_id = A.id
                JOIN cinema C ON A.Cinema_id = c.id
                WHERE c.name = (%s) AND S.Screening_Start > NOW()
                ORDER BY M.title, S.Screening_Start""", (session['cinema_name'],))

    film_times = cur.fetchall()
    times = {}
    for t in film_times:
        if t[0] not in times.keys():
            times[t[0]] = [(t[1].strftime('%Y-%m-%d::%H-%M'), t[2])]
        else:
            times[t[0]].append((t[1].strftime('%Y-%m-%d::%H-%M'), t[2]))

    return render_template('cinemabase.html', cinemaName=session['cinema_name'],
                           filmTimes=times.items())


@bp_booking.route('foo/<screening>',  methods=["GET", "POST"])
def seat_select(screening):
    cur = db.connection.cursor()
    cur.execute("""SELECT M.title, S.Screening_Start
                    FROM screening S JOIN movie M ON s.movie_id = M.id
                    WHERE S.id = (%s)""", (screening,))
    screening_details = cur.fetchone()
    title = screening_details[0]
    time = screening_details[1].strftime('%d %B  %H:%M')
    cur.execute("""SELECT A.row_count, A.column_count
                    FROM auditorium A JOIN screening S on S.auditorium_id = A.id
                    WHERE S.id = (%s)""", (screening,))
    screen_no = cur.fetchone()
    row = screen_no[0]
    column = screen_no[1]




    return render_template('booking/seatSelect.html', screeningId=screening,
                           title=title, time=time, rows=row, columns=column)


@bp_booking.route('/processticket', methods=['GET', 'POST'])
def process_ticket():
    ticket_value = request.form.get('hidden-ticket-value')

    ## insert into database here
    return 'Ticket inserted into database' + ticket_value
