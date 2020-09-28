from flask_mongoengine import Document
from mongoengine import StringField, ListField, ReferenceField, PULL


class Congregation(Document):
    name = StringField(required=True)
    volunteers = ListField(ReferenceField("User"), default=[])
    shifts = ListField(ReferenceField("Shift"), default=[])
