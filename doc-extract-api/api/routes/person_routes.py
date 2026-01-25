from flask import Blueprint, request, jsonify
from api.models import db, Person
from services.person_service import PersonService
from utils import not_found_if_none

person_bp = Blueprint('persons', __name__)

@person_bp.route('', methods=['POST'])
def create_person():
    data = request.get_json()
    person = PersonService.create_person(**data)
    if person is None:
        return jsonify({"error": "Failed to create person"}), 400
    return jsonify(person.to_dict()), 201

@person_bp.route('', methods=['GET'])
@not_found_if_none
def list_persons():
    return PersonService.list_persons()

@person_bp.route('/<int:person_id>', methods=['GET'])
@not_found_if_none
def get_person(person_id):
    return PersonService.get_person_by_id(person_id)

@person_bp.route('/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.get_json()
    person = PersonService.update_person(person_id, **data)
    if person is None:
        return jsonify({"error": "Failed to update person"}), 400
    return jsonify(person.to_dict())

@person_bp.route('/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    success = PersonService.delete_person(person_id)
    if not success:
        return jsonify({"error": "Failed to delete person"}), 400
    return jsonify({"message": "Person deleted successfully"}), 200