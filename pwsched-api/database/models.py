from .db import db
from flask_security import UserMixin, RoleMixin


class Congregation(db.Document):
    name = db.StringField(required=True)
    volunteers = db.ListField(db.ReferenceField("User"))


class Shift(db.Document):
    location = db.StringField(required=True)
    time = db.DateTimeField(required=True)
    volunteers = db.ListField(required=True, max_length=2)
    requested_by = db.ListField()


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
