from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField, ListField, ReferenceField


class Shift(Document):
    location = StringField(required=True)
    time = DateTimeField(required=True)
    volunteers = ListField(required=True, max_length=2)
    requested_by = ListField(ReferenceField("User"))
