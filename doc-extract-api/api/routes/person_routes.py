from flask import Blueprint, request, jsonify
from api.models import db, Person
from services.person_service import PersonService

person_bp = Blueprint('persons', __name__)

@person_bp.route('', methods=['POST'])
def create_person():
    data = request.get_json()
    result = PersonService.create_person(**data)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    if result is None:
        return jsonify({"error": "Failed to create person"}), 400
    return jsonify(result.to_dict()), 201

@person_bp.route('', methods=['GET'])
def list_persons():
    persons = PersonService.list_persons()
    return jsonify([p.to_dict() for p in persons])

@person_bp.route('/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = PersonService.get_person_by_id(person_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.to_dict())

@person_bp.route('/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.get_json()
    result = PersonService.update_person(person_id, **data)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    if result is None:
        return jsonify({"error": "Failed to update person"}), 400
    return jsonify(result.to_dict())

@person_bp.route('/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    success = PersonService.delete_person(person_id)
    if not success:
        return jsonify({"error": "Failed to delete person"}), 400
    return jsonify({"message": "Person deleted successfully"}), 200