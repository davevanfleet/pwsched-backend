from flask import Response, make_response, request, Blueprint, jsonify
from flask_restful import Resource
from flask_security import MongoEngineUserDatastore, hash_password, \
                            verify_password, login_user, current_user, \
                            logout_user
import json
import jwt
import os
from database.models import User, Role
from database.db import db
from IPython import embed

user_datastore = MongoEngineUserDatastore(db, User, Role)


# class UserApi(Resource):
#     def get(self, id):
#         user = User.objects().get(id=id).to_json()
#         return Response(user, mimetype="application/json", status=200)

#     def put(self, id):
#         body = request.get_json()
#         User.objects().get(id=id).update(**body)
#         return '', 200

#     def delete(self, id):
#         User.objects().get(id=id).delete()
#         return '', 200


# class UsersApi(Resource):
#     def get(self):
#         users = User.objects().to_json()
#         return Response(users, mimetype="application/json", status=200)

#     def post(self):
#         body = request.get_json()
#         email = body["email"]
#         password = body["password"]
#         user = user_datastore.create_user(email=email,
#                                           password=hash_password(password))
#         return Response(user, mimetype="application/json", status=200)

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    email = body["email"]
    password = body["password"]
    user = user_datastore.create_user(email=email,
                                      password=hash_password(password))
    login_user(user)
    token = jwt.encode({"email": user.email}, os.environ.get("SECRET_KEY"))
    return (jsonify({"email": user.email}), 200,
            {"Set-Cookie": f'auth={token}'})


sessions_blueprint = Blueprint('sessions', __name__)


@sessions_blueprint.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body["email"]
    password = body["password"]
    user = user_datastore.get_user(email)
    if verify_password(password, user.password):
        login_user(user)
        token = jwt.encode({"email": user.email}, os.environ.get("SECRET_KEY"))
        return (jsonify({"email": user.email}), 200,
                {"Set-Cookie": f'auth={token}'})
    else:
        return jsonify({"error": "unable to login"}), 200


@sessions_blueprint.route('/logout', methods=['POST'])
def logout():
    res = make_response('', 200)
    res.delete_cookie('auth')
    logout_user()
    return res, 200