import os
import flask_wtf
from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from Main.config import Config
from Main.User.models import User
from IPython import embed


db = MongoEngine()
crypt = Bcrypt()
mongo = PyMongo()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = None
login_manager.login_message_category = 'info'


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    crypt.init_app(app)
    login_manager.init_app(app)
    mongo.init_app(app)
    mail.init_app(app)

    from Main.Congregation.views import congregations
    from Main.Shift.views import shifts
    from Main.User.views import users_blueprint, sessions_blueprint
    app.register_blueprint(congregations, url_prefix='/congregations')
    app.register_blueprint(shifts, url_prefix='/shifts')
    app.register_blueprint(sessions_blueprint)
    app.register_blueprint(users_blueprint)

    flask_wtf.CSRFProtect(app)
    CORS(app, supports_credentials=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
