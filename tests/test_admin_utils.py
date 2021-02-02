import pytest
from flask import g, session
from bookingsystem.extensions import db

@pytest.mark.run(order=1)
def test_add_cinema(client, auth, app):
    auth.login(username='admin', password='1234')
    assert client.get('/adminutils/addcinema').status_code == 200
    client.post('/adminutils/addcinema', data={'name': 'Testing Cinema', 'address1': 'Inv', 'address2': 'Erness',
                                               'city': 'Inverness', 'county' : 'Ross-shire', 'postcode': 'IN43 Q4B'})

    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT MAX(id) FROM cinema""")
        expected_id = cur.fetchone()[0]
        cur.execute("""SELECT id FROM cinema WHERE name='Testing Cinema' """)
        retrieved_id = cur.fetchone()[0]
        assert expected_id == retrieved_id

@pytest.mark.run(order=2)
def test_add_screen(client, auth, app):
    auth.login(username='admin', password='1234')
    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT id FROM cinema WHERE name='Testing Cinema' """)
        retrieved_id = str(cur.fetchone()[0])

    assert client.get('/adminutils/addscreens').status_code == 200
    client.post('/adminutils/addscreens', data={'name': '1', 'row_count': '10', 'column_count': '10',
                                               'cinemas': retrieved_id})

    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT * FROM auditorium WHERE cinema_id=(%s)""", (retrieved_id,))
        created_auditorium = cur.fetchone()
        assert created_auditorium is not None
        cur.execute("""DELETE FROM cinema WHERE name='Inverness' """)

@pytest.mark.run(order=3)
def test_add_film_manually(client, auth, app):
    auth.login(username='admin', password='1234')
    assert client.get('/adminutils/addcinema').status_code == 200
    client.post('/adminutils/addfilm', data={'imdb_id': '', 'title': 'The Big Lebowski', 'director': ' Joel Coen',
                                            'description': 'Jeff "The Dude" Lebowski, mistaken for a millionaire '
                                                           'of the same name, seeks ''restitution for his ruined '
                                                           'rug and enlists his bowling buddies to help get it.',
                                            'duration': '117', 'movie_image': ''})

    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT * FROM movie WHERE title='The Big Lebowski' """)
        film = cur.fetchone()
        assert film is not None


@pytest.mark.run(order=4)
def test_add_film_imdb(client, auth, app):
    auth.login(username='admin', password='1234')
    assert client.get('/adminutils/addcinema').status_code == 200
    client.post('/adminutils/addfilm', data={'imdb_id': '0088763', 'title': '', 'director': '',
                                            'description': '',
                                            'duration': '', 'movie_image': ''})

    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT * FROM movie WHERE title='Back to the Future' """)
        film = cur.fetchone()
        assert film is not None

@pytest.mark.run(order=5)
def test_create_screening(client, auth, app):
    auth.login(username='admin', password='1234')
    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT id FROM cinema WHERE name='Testing Cinema'""")
        cinema_id = cur.fetchone()[0]
        cur.execute("""SELECT id FROM auditorium WHERE cinema_id=(%s)""", (cinema_id, ))
        screen_id = cur.fetchone()[0]

        cur.execute("""SELECT id FROM movie WHERE title='The Big Lebowski'""")
        movie_id = cur.fetchone()[0]

    assert client.get('/adminutils/createscreening').status_code == 200
    # change time each TIME
    client.post('/adminutils/createscreening', data={'screen': screen_id, 'films': movie_id,
                                                     'film_time': '2026-07-12T12:22',})

@pytest.mark.run(order=6)
def test_delete_auditorium(client, auth, app):
    auth.login(username='admin', password='1234')
    with app.app_context():
        # Setup
        cur = db.connection.cursor()
        cur.execute("""SELECT id FROM cinema WHERE name='Testing Cinema'""")
        cinema_id = str(cur.fetchone()[0])
        cur.execute("""SELECT id FROM auditorium WHERE  cinema_id=(%s)""", (cinema_id,))
        auditorium_id = str(cur.fetchone()[0])

        # Check that auditorium exists
        cur.execute("""SELECT * FROM auditorium WHERE cinema_id=(%s)""", (cinema_id,))
        deleted_cinema = cur.fetchone()
        assert deleted_cinema

    # Post auditorium id to our deletion URL and check that it no longer exists
    assert client.get('/adminutils/makedeletions').status_code == 200
    client.post('/adminutils/makedeletions', data = {'auditoriums':  auditorium_id})
    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT * FROM auditorium WHERE cinema_id=(%s)""", (cinema_id,))
        deleted_cinema = cur.fetchone()
        assert deleted_cinema is None

@pytest.mark.run(order=7)
def test_delete_cinema(client, auth, app):
    auth.login(username='admin', password='1234')
    with app.app_context():
        # Check that cinema exists
        cur = db.connection.cursor()
        cur.execute("""SELECT id FROM cinema WHERE name='Testing Cinema'""")
        cinema_id = cur.fetchone()[0]
        assert cinema_id

    # Post auditorium id to our deletion URL and check that it no longer exists
    assert client.get('/adminutils/makedeletions').status_code == 200
    client.post('/adminutils/makedeletions', data={'cinemas': cinema_id})
    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT id FROM cinema WHERE name='Testing Cinema'""")
        cinema_id = cur.fetchone()[0]
        assert cinema_id is None

@pytest.mark.run(order=8)
def test_delete_cinema(client, auth, app):
    auth.login(username='admin', password='1234')
    with app.app_context():
        # Check that cinema exists
        cur = db.connection.cursor()
        cur.execute("""SELECT id FROM movie WHERE Title='The Big Lebowski' """)
        film_id = str(cur.fetchone()[0])
        assert film_id

    # Post auditorium id to our deletion URL and check that it no longer exists
    assert client.get('/adminutils/makedeletions').status_code == 200
    client.post('/adminutils/makedeletions', data={'movies': film_id})
    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""SELECT * FROM movie WHERE id=(%s)""", (film_id,))
        deleted_film = cur.fetchone()
        assert deleted_film is None

