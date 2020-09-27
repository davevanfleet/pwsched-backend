from flask import Blueprint, request, jsonify
from .models import Shift
from Main.utils import *

shifts = Blueprint('shifts', __name__)


@shifts.route('/<id>', methods=['GET'])
def get_shift(cong_id, id):
    congregation = set_congregation(cong_id)
    shift = Shift.objects().get(id=id)
    return jsonify(shift), 200


@shifts.route('/<id>', methods=['PUT'])
def update_shift(cong_id, id):
    congregation = set_congregation(cong_id)
    body = request.get_json()
    shift = Shift.objects().get(id=id).update(**body)
    return jsonify(shift), 200


@shifts.route('/<id>', methods=['DELETE'])
def delete_shift(cong_id, id):
    congregation = set_congregation(cong_id)
    Shift.objects().get(id=id).delete()
    return jsonify({"message": "deleted shift"}), 200


@shifts.route('/', methods=['GET'])
def get_shifts(cong_id):
    congregation = set_congregation(cong_id)
    shifts = congregation.shifts
    return jsonify(shifts), 200


@shifts.route('/', methods=['POST'])
def create_shift():
    congregation = set_congregation(cong_id)
    body = request.get_json()
    shift_time = datetime.strptime(body["datetime"], '%Y-%m-%dT%H:%M')
    shift = Shift(
        location=body["location"],
        datetime=shift_time
    )
    return jsonify(shift), 200
