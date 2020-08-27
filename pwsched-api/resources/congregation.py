from flask import Response, request
from flask_restful import Resource
from flask_restful_swagger import swagger
from database.models import Congregation


class CongregationApi(Resource):
    @swagger.operation(
        notes='This endpoint provides the congregation record based on a \
            given id',
        responseClass=Congregation.__name__,
        nickname='GET Congregation',
        parameters=[
            {
              "name": "id",
              "description": "id of congregation stored in database",
              "required": True,
              "allowMultiple": False,
              "dataType": "String",
              "paramType": "body"
            }
          ],
        responseMessages=[
            {
              "code": 200,
              "message": "Success"
            }
          ]
        )
    def get(self, id):
        congregation = Congregation.objects().get(id=id).to_json()
        return Response(congregation, mimetype="application/json", status=200)

    @swagger.operation(
        notes='This endpoint updates a congregation record',
        responseClass=Congregation.__name__,
        nickname='PUT Congregation',
        parameters=[
            {
              "name": "id",
              "description": "id of congregation stored in database",
              "required": True,
              "allowMultiple": False,
              "dataType": "String",
              "paramType": "body"
            },
            {
              "name": "name",
              "description": "updated name for congregation record",
              "required": False,
              "allowMultiple": False,
              "dataType": "String",
              "paramType": "body"
            }
          ],
        responseMessages=[
            {
              "code": 200,
              "message": "Success"
            }
          ]
        )
    def put(self, id):
        body = request.get_json()
        Congregation.objects().get(id=id).update(**body)
        return '', 200

    @swagger.operation(
        notes='This endpoint deletes a congregation record',
        responseClass=Congregation.__name__,
        nickname='DELETE Congregation',
        parameters=[
            {
              "name": "id",
              "description": "id of congregation stored in database",
              "required": True,
              "allowMultiple": False,
              "dataType": "String",
              "paramType": "body"
            }
          ],
        responseMessages=[
            {
              "code": 200,
              "message": "Success"
            }
          ]
        )
    def delete(self, id):
        Congregation.objects().get(id=id).delete()
        return '', 200


class CongregationsApi(Resource):
    @swagger.operation(
        notes='This endpoint returns all congregation records',
        responseClass=Congregation.__name__,
        nickname='GET Congregations',
        parameters=[],
        responseMessages=[
            {
              "code": 200,
              "message": "Success"
            }
          ]
        )
    def get(self):
        congregations = Congregation.objects().to_json()
        return Response(congregations, mimetype="application/json", status=200)

    @swagger.operation(
        notes='This endpoint creates a new congregation record',
        responseClass=Congregation.__name__,
        nickname='POST Congregations',
        parameters=[
            {
              "name": "id",
              "description": "id of congregation stored in database",
              "required": True,
              "allowMultiple": False,
              "dataType": "String",
              "paramType": "body"
            },
            {
              "name": "name",
              "description": "updated name for congregation record",
              "required": True,
              "allowMultiple": False,
              "dataType": "String",
              "paramType": "body"
            }
          ],
        responseMessages=[
            {
              "code": 200,
              "message": "Success"
            }
          ]
        )
    def post(self):
        body = request.get_json()
        congregation = Congregation(**body).save()
        id = congregation.id
        return {'id': str(id)}, 200
