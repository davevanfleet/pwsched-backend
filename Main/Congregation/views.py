from flask import Blueprint, jsonify, request
from .models import Congregation

congregations = Blueprint('congregations', __name__)


@congregations.route('/<id>', methods=['GET'])
def get_congregation(id):
    congregation = Congregation.objects().get(id=id)
    return jsonify(congregation), 200


@congregations.route('/<id>', methods=['PUT'])
def update_congregation(id):
    body = request.get_json()
    Congregation.objects().get(id=id).update(**body)
    congregation = Congregation.objects().get(id=id)
    return jsonify(congregation), 200


@congregations.route('/<id>', methods=['DELETE'])
def delete_congregation(id):
    Congregation.objects().get(id=id).delete()
    return jsonify({"message": "congregation deleted"}), 200


@congregations.route('/', methods=['GET'])
def get_congregations():
    congregations = Congregation.objects()
    return jsonify(congregations), 200


@congregations.route('/', methods=['POST'])
def create_congregation():
    body = request.get_json()
    congregation = Congregation(name=body['name']).save()
    return jsonify(congregation), 200
