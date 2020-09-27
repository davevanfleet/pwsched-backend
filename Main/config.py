from os import environ, path
from dotenv import load_dotenv


class Config(object):
    SECRET_KEY = environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_CSRF_COOKIE = {"key": "XSRF-TOKEN"}
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_CHECK_DEFAULT = False
    MONGODB_SETTINGS = {
        'host': environ.get("MONGODB_SETTINGS")
    }
    MONGO_URI = environ.get("MONGO_URI")


class TestConfig(object):
    SECRET_KEY = environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_CSRF_COOKIE = {"key": "XSRF-TOKEN"}
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_CHECK_DEFAULT = False
    MONGODB_SETTINGS = {
        'host': "PLEAASSSEEWOOOORK!"
    }
    MONGO_URI = environ.get("TEST_MONGO_URI")
    TESTING = True
