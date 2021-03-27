import os
import tempfile
import pytest
from bookingsystem import create_app
from bookingsystem.extensions import db



@pytest.fixture
def app():

    app = create_app({
        'TESTING': True,
    })

    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""DELETE FROM user WHERE is_admin=0""")
        cur.execute("""INSERT INTO user (username, password, email, first_name, last_name, is_admin)
                        VALUES
                        ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 
                        'test@mail.com', 'John', 'Doe', '0'),
                        ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79',
                        'other@mail.com', 'Foo','Bar', '0');
                        """)
        db.connection.commit()
        cur.close()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

#
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)


