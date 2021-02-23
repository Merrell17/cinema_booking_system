import pytest
from bookingsystem.extensions import db
from flask import url_for

def test_index(client, auth):
    response = client.get('http://127.0.0.1:5000/booking/selectcinema')
    assert b"Log In" in response.data
    assert b"Register" in response.data
    auth.login()
    response = client.get('http://127.0.0.1:5000/booking/selectcinema')
    assert b'Log Out' in response.data

@pytest.mark.parametrize('path', (
    #'/booking/myaccount',
    '/booking/processticket/40/80/',

))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'

