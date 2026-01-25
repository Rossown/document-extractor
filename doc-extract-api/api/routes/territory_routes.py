from flask import Blueprint, request, jsonify
from services.territory_service import TerritoryService

territory_bp = Blueprint('territories', __name__)

@territory_bp.route('', methods=['POST'])
def create_territory():
    data = request.get_json()
    result = TerritoryService.create_territory(data.get('name'), data.get('country-region-code'), data.get('group'))
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    if result is None:
        return jsonify({"error": "Failed to create territory"}), 400
    return jsonify(result.to_dict()), 201

@territory_bp.route('', methods=['GET'])
def list_territories():
    territories = TerritoryService.list_territories()
    return jsonify([t.to_dict() for t in territories])

@territory_bp.route('/<int:territory_id>', methods=['GET'])
def get_territory(territory_id):
    territory = TerritoryService.get_territory_by_id(territory_id)
    return jsonify(territory.to_dict())

@territory_bp.route('/<int:territory_id>', methods=['PUT'])
def update_territory(territory_id):
    data = request.get_json()
    result = TerritoryService.update_territory(territory_id, data.get('name'), data.get('country-region-code'), data.get('group'))
    return jsonify(result.to_dict()), 200

@territory_bp.route('/<int:territory_id>', methods=['DELETE'])
def delete_territory(territory_id):
    TerritoryService.delete_territory(territory_id)
    return jsonify({"message": "Sales territory deleted"}), 204