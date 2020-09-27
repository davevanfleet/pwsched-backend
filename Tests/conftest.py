# import os
# import pytest
# from flask_mongoengine import MongoEngine
# from flask_pymongo import PyMongo
# from flask_mail import Mail
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from Main import create_app
# from Main.config import TestConfig
# from IPython import embed

# db = MongoEngine()
# crypt = Bcrypt()
# mongo = PyMongo()
# mail = Mail()

# login_manager = LoginManager()
# login_manager.login_view = None
# login_manager.login_message_category = 'info'


# @pytest.fixture
# def app():
#     app = create_app({
#         "SECRET_KEY": 'test_secret',
#         "SECURITY_PASSWORD_SALT": 'test-salt',
#         "SECURITY_CSRF_COOKIE": {"key": "XSRF-TOKEN"},
#         "SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS": True,
#         "WTF_CSRF_TIME_LIMIT": None,
#         "WTF_CSRF_CHECK_DEFAULT": False,
#         "MONGODB_SETTINGS": {
#             'host': "PLEAASSSEEWOOOORK!"
#         },
#         "MONGO_URI": "PLEAASSSEEWOOOORK!",
#         "TESTING": True
#     })

#     db.init_app(app)
#     crypt.init_app(app)
#     login_manager.init_app(app)
#     mongo.init_app(app)
#     mail.init_app(app)

#     yield app


# @pytest.fixture
# def client(app):
#     return app.test_client()


# @pytest.fixture
# def runner(app):
#     return app.test_cli_runner()
