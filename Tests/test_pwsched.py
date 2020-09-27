import os
import pytest
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from Main import create_app
from Main.Congregation.models import Congregation

db = MongoEngine()
crypt = Bcrypt()
mongo = PyMongo()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = None
login_manager.login_message_category = 'info'


@pytest.fixture
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

    yield app

    Congregation.objects().delete()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_ping(client):
    rv = client.get('/ping')
    assert b'Hello, World!' in rv.data


def test_create_congregation(client):
    congregation = Congregation(
        name="Test Congregation"
    )
    assert congregation.name == "Test Congregation"
    congregation.save()
    assert (Congregation.objects(name="Test Congregation")
            .first().name == "Test Congregation")
