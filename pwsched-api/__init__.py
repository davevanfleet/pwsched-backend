import os
from flask import Flask
from flask_restful import Api
from flask_security import Security
import flask_wtf
from database.db import initialize_db
from database.models import User, Role
from resources.auth import user_datastore, sessions_blueprint
from resources.routes import initialize_routes


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SECURITY_PASSWORD_SALT=os.environ.get("SECURITY_PASSWORD_SALT"),
        SECURITY_CSRF_COOKIE={"key": "XSRF-TOKEN"},
        SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS=True,
        WTF_CSRF_TIME_LIMIT=None,
        WTF_CSRF_CHECK_DEFAULT=False
    )
    api = Api(app)
    initialize_db(app)
    initialize_routes(api)
    app.register_blueprint(sessions_blueprint)
    security = Security(app, user_datastore, register_blueprint=False)
    flask_wtf.CSRFProtect(app)

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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
