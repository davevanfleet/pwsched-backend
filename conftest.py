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


@pytest.fixture(autouse=True)
def app():
    db = MongoEngine()
    crypt = Bcrypt()
    mongo = PyMongo()
    mail = Mail()

    login_manager = LoginManager()
    login_manager.login_view = None
    login_manager.login_message_category = 'info'

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

    congregation = Congregation(name="English - Willimantic").save()
    shift = Shift(location="UConn",
                  datetime=datetime.now,
                  congregation=congregation.to_dbref()).save()
    congregation.shifts.append(shift.to_dbref())
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
