from flask_mongoengine import Document
from mongoengine import StringField, ListField, ReferenceField


class Congregation(Document):
    name = StringField(required=True)
    volunteers = ListField(ReferenceField("User"), default=[])
