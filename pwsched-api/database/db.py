from flask_mongoengine import MongoEngine
from flask_security import Security, MongoEngineUserDatastore

db = MongoEngine()


def initialize_db(app):
    db.init_app(app)
    from .models import User, Role
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
