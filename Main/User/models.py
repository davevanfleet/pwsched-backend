from flask import current_app
from flask_login import UserMixin
from _datetime import datetime
from flask_mongoengine import Document
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from mongoengine import IntField, ListField, BooleanField, DateTimeField, \
    EmbeddedDocument, EmbeddedDocumentField, DictField, EmailField, \
    EmbeddedDocumentListField, StringField, ReferenceField
from Main import login_manager


class Meta(EmbeddedDocument):
    date_added = DateTimeField(default=datetime.utcnow)
    timestamps = ListField(DateTimeField())


class User(Document, UserMixin):
    user_meta = EmbeddedDocumentField(Meta, default=Meta)
    name = StringField(required=True, max_length=50)
    email = EmailField(required=True, unique=True)
    role = StringField(default="volunteer")
    confirmed = BooleanField(default=False)
    password = StringField(min_length=8, required=True)
    congregation = ReferenceField('Congregation', required=True)
    isActive = BooleanField(default=True)
    shifts = ListField(ReferenceField('Shift'), default=[])

    def get_auth_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': str(self.id), 'email': self.email}).decode('utf-8')
  
    @login_manager.user_loader
    def load_user(id):
        return User.objects(id=id).first()

    # User mixin methods
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
