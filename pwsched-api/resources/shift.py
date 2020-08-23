from flask import Response, request
from flask_restful import Resource
from database.models import Shift


class ShiftApi(Resouce):
    def get(self, id):
        shift = Shift.objects().get(id=id).to_json()
        return Response(shift, mimetype="application/json", status=200)

    def put(self, id):
        body = request.get_json()
        Shift.objects().get(id=id).update(**body)
        return '', 200

    def delete(self, id):
        Shift.objects().get(id=id).delete()
        return '', 200


class ShiftsApi(Resource):
    def get(self):
        shifts = Shift.objects().to_json()
        return Response(shifts, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        shift = Shift(**body).save()
        id = shift.id
        return {'id': str(id)}, 200
