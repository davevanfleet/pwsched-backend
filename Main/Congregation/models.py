from flask_mongoengine import Document
from mongoengine import StringField, ListField, ReferenceField, \
    EmbeddedDocumentListField
from Main.Shift.models import Shift


class Congregation(Document):
    name = StringField(required=True)
    volunteers = ListField(ReferenceField("User"), default=[])
    shifts = EmbeddedDocumentListField(Shift, default=[])
