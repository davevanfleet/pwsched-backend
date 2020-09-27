from flask import current_app, jsonify, redirect, request
from flask_login import current_user
from functools import wraps
from Main.User.models import User
from Main.Congregation.models import Congregation
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def set_user(id):
    user = User.objects().get(id=id)
    return user


def set_congregation(id):
    congregation = Congregation.objects().get(id=id)
    return congregation


def decode_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.loads(token)


def confirmation_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.confirmed:
            return jsonify({"message": "Email conirmation required"}), 401
        return func(*args, **kwargs)
    return decorated_view
