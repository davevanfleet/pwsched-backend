import pytest
from datetime import datetime
from Main.Congregation.models import Congregation
from Main.Shift.models import Shift
from Main.User.models import User
from flask_login import current_user, logout_user


def test_login(client):
    payload = {"email": "fake@fakemail.com",
               "password": "password"}
    response = client.post('/login', json=payload)
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    data = response.get_json()
    assert data['user']['name'] == "Brother Service Overseer"


def test_register(client, monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "testsecret")
    payload = {"name": "Sister Pioneer",
               "email": "email@email.com",
               "password": "password",
               "congregation": "English - Willimantic"}
    response = client.post('/register', json=payload)
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers


def test_get_current_user(app, client, monkeypatch):
    with app.test_request_context():
        monkeypatch.setenv("SECRET_KEY", "testsecret")
        response = client.post('/get_current_user')
        assert response.status_code == 401
        user = User.objects(email='fake@fakemail.com').first()
        token = user.get_auth_token()
        client.set_cookie('localhost', 'auth', token)
        response = client.post('/get_current_user')
        assert response.status_code == 200
