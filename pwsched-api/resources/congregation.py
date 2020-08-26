from flask import Response, request
from flask_restful import Resource
from database.models import Congregation


class CongregationApi(Resource):
    def get(self, id):
        congregation = Congregation.objects().get(id=id).to_json()
        return Response(congregation, mimetype="application/json", status=200)

    def put(self, id):
        body = request.get_json()
        Congregation.objects().get(id=id).update(**body)
        return '', 200

    def delete(self, id):
        Congregation.objects().get(id=id).delete()
        return '', 200


class CongregationsApi(Resource):
    def get(self):
        congregations = Congregation.objects().to_json()
        return Response(congregations, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        congregation = Congregation(**body).save()
        id = congregation.id
        return {'id': str(id)}, 200
