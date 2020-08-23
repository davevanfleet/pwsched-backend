from .db import db


class Congregation(db.Document):
    name = db.StringField(required=True)


class Shift(db.Document):
    location = db.StringField(required=True)
    time = db.DateTimeField(required=True)
    volunteers = db.ListField(required=True, max_length=2)
    requested_by = db.ListField()
