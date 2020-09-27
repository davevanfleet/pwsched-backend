import jwt
import os
from _datetime import datetime
from flask import Blueprint, request, make_response, jsonify
from flask_login import login_user, logout_user
from .models import User
from Main import crypt
from Main.Congregation.models import Congregation
from Main.utils import *
from IPython import embed

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    email = body["email"]
    password = body["password"]
    name = body["name"]
    hashed_password = (crypt.generate_password_hash(password)
                       .decode('utf-8'))
    congregation = Congregation.objects().get(name=body["congregation"])
    user = User(email=email,
                password=hashed_password,
                name=name,
                congregation=congregation.to_dbref())
    user.save()
    login_user(user)
    token = (
        jwt.encode({"email": user.email}, os.environ.get("SECRET_KEY"))
        .decode('utf-8')
    )
    return (jsonify({"user": user}), 200,
            {"Set-Cookie": f'auth={token}'})


sessions_blueprint = Blueprint('sessions', __name__)


@sessions_blueprint.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body["email"]
    password = body["password"]
    user = User.objects(email=email).first()
    if user and crypt.check_password_hash(user.password, password):
        login_user(user)
        user.user_meta.timestamps.append(datetime.utcnow)
        user.save()
        token = user.get_auth_token()
        res = make_response(jsonify({"user": user}), 200)
        res.set_cookie('user-auth', value=token, path='/')
        return res
    else:
        return jsonify({"error": "unable to login"}), 401


@sessions_blueprint.route('/logout', methods=['POST'])
def logout():
    res = make_response(jsonify({"message": "successfully logged out"}), 200)
    res.delete_cookie('user-auth')
    logout_user()
    return res, 200


@sessions_blueprint.route('/get_current_user', methods=['POST'])
def get_current_user():
    token = request.cookies["auth"]
    email = jwt.decode(token, os.environ.get("SECRET_KEY"))['email']
    user = User.objects(email=email).first()
    if user:
        login_user(user)
        return jsonify({"user": {"email": user.email}}), 200
    else:
        return jsonify({"message": "unable to find user"}), 401
