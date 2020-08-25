import os
from flask import Flask
from flask_restful import Api
from flask_security import Security
from database.db import initialize_db
from database.models import User, Role
from resources.user import user_datastore
from resources.routes import initialize_routes


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SECURITY_PASSWORD_SALT=os.environ.get("SECURITY_PASSWORD_SALT"),
    )
    api = Api(app)
    initialize_db(app)
    initialize_routes(api)
    security = Security(app, user_datastore)

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
