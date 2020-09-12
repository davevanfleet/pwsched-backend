from flask_mongoengine import Document
from mongoengine import StringField, BooleanField, DateTimeField, ListField,\
    ReferenceField
from flask_security import UserMixin, RoleMixin


class Role(Document, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)


class User(Document, UserMixin):
    email = StringField(max_length=255)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])
