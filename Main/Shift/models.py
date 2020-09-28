from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField, ListField, ReferenceField


class Shift(Document):
    location = StringField(required=True)
    datetime = DateTimeField(required=True)
    congregation = ReferenceField("Congregation")
    volunteers = ListField(ReferenceField("User"), max_length=2, default=[])
    requested_by = ListField(ReferenceField("User"), default=[])
