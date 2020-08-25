from flask import Response, request
from flask_restful import Resource
from flask_security import MongoEngineUserDatastore, hash_password
from database.models import User, Role
from database.db import db
from IPython import embed

user_datastore = MongoEngineUserDatastore(db, User, Role)


class UserApi(Resource):
    def get(self, id):
        user = User.objects().get(id=id).to_json()
        return Response(user, mimetype="application/json", status=200)

    def put(self, id):
        body = request.get_json()
        User.objects().get(id=id).update(**body)
        return '', 200

    def delete(self, id):
        User.objects().get(id=id).delete()
        return '', 200


class UsersApi(Resource):
    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        email = body["email"]
        password = body["password"]
        user = user_datastore.create_user(email=email,
                                          password=hash_password(password))
        return Response(user, mimetype="application/json", status=200)
