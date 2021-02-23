import pytest
from flask import g, session
from bookingsystem.extensions import db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a', 'email': 'ab@example.com',
                                'fname': 'a', 'lname': 'b'}
    )
    # Check we're being redirected to the login page after registering
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        cur = db.connection.cursor()
        cur.execute(
            "select * from user where username = 'a'",
        )
        assert cur.fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'email', 'fname', 'lname' ), (
    ('', '', '', '',''),
    ('a', '', '', '', '' ),
    ('a', 'b','', '', '' ),
    ('test', 'test', 'test@mail.com', 'john', 'Doe'),
))
def test_register_validate_input(client, username, password, email, fname, lname,):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password, 'email': email, 'fname': fname, 'lname': lname }
    )


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    with client:
        client.get('/')
        assert session['user_id'] != 0
        assert g.user is not None


def test_admin_login(client, auth, app):
    auth.login(username='admin', password='1234')
    with client:
        client.get('/')
        assert g.admin is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'wrongPW', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    # Check that the user has not been redirected to homepage/successfully logged in
    with pytest.raises(AttributeError):
        response.header['location']


def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session

