from flask import Blueprint, request, jsonify
from .models import Shift

shifts = Blueprint('shifts', __name__)


@shifts.route('/<id>', methods=['GET'])
def get_shift(id):
    shift = Shift.objects().get(id=id)
    return jsonify(shift), 200


@shifts.route('/<id>', methods=['PUT'])
def update_shift(id):
    body = request.get_json()
    shift = Shift.objects().get(id=id).update(**body)
    return jsonify(shift), 200


@shifts.route('/<id>', methods=['DELETE'])
def delete_shift(id):
    Shift.objects().get(id=id).delete()
    return jsonify({"message": "deleted shift"}), 200


@shifts.route('/', methods=['GET'])
def get_shifts():
    shifts = Shift.objects()
    return jsonify(shifts), 200


@shifts.route('/', methods=['POST'])
def create_shift():
    body = request.get_json()
    shift = Shift(**body).save()
    return jsonify(shift), 200
