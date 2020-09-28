from datetime import datetime
from flask import Blueprint, request, jsonify
from .models import Shift
from Main.utils import *

shifts = Blueprint('shifts', __name__)


@shifts.route('/<id>', methods=['GET'])
def get_shift(cong_id, id):
    congregation = set_congregation(cong_id)
    shift = Shift.objects().get(id=id)
    if shift.congregation.id != congregation.id:
        return (jsonify({"message":
                         "shift does not belong to this congregation"}),
                401)
    else:
        return jsonify(shift), 200


@shifts.route('/<id>', methods=['PUT'])
def update_shift(cong_id, id):
    congregation = set_congregation(cong_id)
    body = request.get_json()
    Shift.objects().get(id=id).update(**body)
    shift = Shift.objects().get(id=id)
    return jsonify(shift), 200


@shifts.route('/<id>', methods=['DELETE'])
def delete_shift(cong_id, id):
    congregation = set_congregation(cong_id)
    shift = Shift.objects().get(id=id)
    congregation.update(pull__shifts=shift)
    shift.delete()
    return jsonify({"message": "deleted shift"}), 200


@shifts.route('/', methods=['GET'])
def get_shifts(cong_id):
    congregation = set_congregation(cong_id)
    shifts = congregation.shifts
    return jsonify(shifts), 200


@shifts.route('/', methods=['POST'])
def create_shift(cong_id):
    congregation = set_congregation(cong_id)
    body = request.get_json()
    shift_time = datetime.strptime(body["datetime"], '%Y-%m-%dT%H:%M')
    shift = Shift(
        location=body["location"],
        datetime=shift_time,
        congregation=congregation.to_dbref()
    )
    shift.save()
    congregation.shifts.append(shift.to_dbref())
    congregation.save()
    return jsonify(shift), 200
