from flask import Blueprint, request, jsonify
from services.territory_service import TerritoryService
from utils import not_found_if_none

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
@not_found_if_none
def list_territories():
    return TerritoryService.list_territories()

@territory_bp.route('/<int:territory_id>', methods=['GET'])
@not_found_if_none
def get_territory(territory_id):
    return TerritoryService.get_territory_by_id(territory_id)

@territory_bp.route('/<int:territory_id>', methods=['PUT'])
def update_territory(territory_id):
    data = request.get_json()
    result = TerritoryService.update_territory(territory_id, data.get('name'), data.get('country-region-code'), data.get('group'))
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    if not result:
        return jsonify({"error": "Sales territory not found"}), 404
    return jsonify(result.to_dict()), 200

@territory_bp.route('/<int:territory_id>', methods=['DELETE'])
def delete_territory(territory_id):
    success = TerritoryService.delete_territory(territory_id)
    if not success:
        return jsonify({"error": "Sales territory not found"}), 404
    return jsonify({"message": "Sales territory deleted"}), 200