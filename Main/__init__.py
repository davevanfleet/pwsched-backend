import os
import flask_wtf
from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from flask_swagger_ui import get_swaggerui_blueprint
from Main.config import Config
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
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        print(test_config)
        app.config.from_mapping(test_config)

    db.init_app(app)
    crypt.init_app(app)
    login_manager.init_app(app)
    mongo.init_app(app)
    mail.init_app(app)

    from Main.Congregation.views import congregations
    from Main.Shift.views import shifts
    from Main.User.views import users_blueprint, sessions_blueprint
    app.register_blueprint(congregations, url_prefix='/congregations')
    app.register_blueprint(shifts,
                           url_prefix='/congregations/<cong_id>/shifts')
    app.register_blueprint(sessions_blueprint)
    app.register_blueprint(users_blueprint)

    flask_wtf.CSRFProtect(app)
    CORS(app, supports_credentials=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "PWSched API"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/ping', methods=['GET'])
    def ping():
        return "Hello, World!"

    return app
