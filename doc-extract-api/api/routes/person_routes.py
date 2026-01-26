from flask import Blueprint, request, jsonify
from api.models import db, Person
from services.person_service import PersonService

person_bp = Blueprint('persons', __name__)

@person_bp.route('', methods=['POST'])
def create_person():
    data = request.get_json()
    result = PersonService.create_person(**data)
    return jsonify(result.to_dict()), 201

@person_bp.route('', methods=['GET'])
def list_persons():
    cursor = request.args.get('cursor', type=int)
    limit = request.args.get('limit', type=int, default=20)
    persons = PersonService.list_persons(cursor_id=cursor, limit=limit)
    return jsonify(persons), 200

@person_bp.route('/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = PersonService.get_person_by_id(person_id)
    return jsonify(person.to_dict()), 200

@person_bp.route('/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.get_json()
    result = PersonService.update_person(person_id, **data)
    return jsonify(result.to_dict()), 200

@person_bp.route('/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    PersonService.delete_person(person_id)
    return jsonify({"message": "Person deleted successfully"}), 204