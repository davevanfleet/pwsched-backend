import os
import pytest
import json
from time import sleep
from datetime import datetime
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from Main import create_app
from Main.Congregation.models import Congregation
from Main.Shift.models import Shift
from Main.User.models import User

db = MongoEngine()
crypt = Bcrypt()
mongo = PyMongo()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = None
login_manager.login_message_category = 'info'


@pytest.fixture(autouse=True)
def app():
    app = create_app({
        "SECRET_KEY": 'test_secret',
        "SECURITY_PASSWORD_SALT": 'test-salt',
        "SECURITY_CSRF_COOKIE": {"key": "XSRF-TOKEN"},
        "SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS": True,
        "WTF_CSRF_TIME_LIMIT": None,
        "WTF_CSRF_CHECK_DEFAULT": False,
        "MONGODB_SETTINGS": {
            'host': 'mongodb://localhost/pwsched-test'
        },
        "MONGO_URI": 'mongodb://localhost/pwsched-test',
        "TESTING": True
    })

    db.init_app(app)
    crypt.init_app(app)
    login_manager.init_app(app)
    mongo.init_app(app)
    mail.init_app(app)

    Congregation(name="English - Willimantic").save()
    Shift(location="UConn",
          datetime=datetime.now).save()
    User(name="Brother Service Overseer",
         email="fake@fakemail.com",
         password="password",
         congregation=(Congregation.objects().order_by('-id')
                       .first().to_dbref())).save()

    yield app

    Congregation.objects().delete()
    Shift.objects().delete()
    User.objects().delete()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_ping(client):
    response = client.get('/ping')
    assert b'Hello, World!' in response.data


# Model Tests
def test_create_congregation(client):
    congregation = Congregation(
        name="Test Congregation"
    )
    assert congregation.name == "Test Congregation"
    congregation.save()
    assert (Congregation.objects().order_by('-id')
            .first().name == "Test Congregation")


def test_create_shift(client):
    shift = Shift(
        location="UConn",
        datetime=datetime.now
    )
    assert shift.location == "UConn"
    shift.save()
    assert (Shift.objects().order_by('-id').first()
            .location == "UConn")


def test_create_user(client):
    user = User(
        name="Spongebob",
        email="fake2@fakemail.com",
        password="password",
        congregation=(Congregation.objects().order_by('-id')
                      .first().to_dbref())
    )
    assert user.email == "fake2@fakemail.com"
    user.save()
    assert (User.objects().order_by('-id').first()
            .email == "fake2@fakemail.com")
    assert (User.objects().order_by('-id').first()
            .congregation.name == "English - Willimantic")


# Endpoints Tests
def test_get_congregations(client):
    response = client.get('/congregations/')
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['name'] == "English - Willimantic"


def test_post_congregations(client):
    payload = {"name": "Columbia"}
    response = client.post('/congregations/',
                           json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == "Columbia"
    response = client.get('/congregations/')
    data = response.get_json()
    assert len(data) == 2
    assert data[1]["name"] == "Columbia"


def test_get_congregation(client):
    cong_id = str(Congregation.objects().first().id)
    response = client.get(f'/congregations/{cong_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "English - Willimantic"


def test_put_congregation(client):
    payload = {"name": "Not Willimantic"}
    cong_id = str(Congregation.objects().first().id)
    response = client.put(f'/congregations/{cong_id}',
                          json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Not Willimantic"


def test_delete_congregation(client):
    cong_id = str(Congregation.objects().first().id)
    response = client.delete(f'/congregations/{cong_id}')
    assert response.status_code == 200
    assert len(Congregation.objects()) == 0
