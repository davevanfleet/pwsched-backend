import jwt
import os
from flask import make_response, request, Blueprint, jsonify
from flask_security import hash_password, verify_password, login_user,\
    current_user, logout_user
from .models import User, Role
from Main.Congregation.models import Congregation
from flask_security import MongoEngineUserDatastore

user_datastore = MongoEngineUserDatastore(db, User, Role)
users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    email = body["email"]
    password = body["password"]
    congregation = Congregation.objects().get(name=body["congregation"])
    user = user_datastore.create_user(email=email,
                                      password=hash_password(password))
    volunteer_role = user_datastore.find_role("Volunteer")
    user_datastore.add_role_to_user(user, volunteer_role)
    login_user(user)
    token = (
        jwt.encode({"email": user.email}, os.environ.get("SECRET_KEY"))
        .decode('utf-8')
    )
    return (jsonify({"user": {"email": user.email}}), 200,
            {"Set-Cookie": f'auth={token}'})


sessions_blueprint = Blueprint('sessions', __name__)


@sessions_blueprint.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body["email"]
    password = body["password"]
    user = user_datastore.get_user(email)
    if user and verify_password(password, user.password):
        login_user(user)
        token = (
            jwt.encode({"email": user.email}, os.environ.get("SECRET_KEY"))
            .decode('utf-8')
        )
        return (jsonify({"user": {"email": user.email}}), 200,
                {"Set-Cookie": f'auth={token}'})
    else:
        return jsonify({"error": "unable to login"}), 401


@sessions_blueprint.route('/logout', methods=['POST'])
def logout():
    res = make_response(jsonify({"message": "successfully logged out"}), 200)
    res.delete_cookie('auth')
    logout_user()
    return res, 200


@sessions_blueprint.route('/get_current_user', methods=['POST'])
def get_current_user():
    token = request.cookies["auth"]
    email = jwt.decode(token, os.environ.get("SECRET_KEY"))['email']
    user = user_datastore.get_user(email)
    login_user(user)
    return jsonify({"user": {"email": user.email}}), 200
