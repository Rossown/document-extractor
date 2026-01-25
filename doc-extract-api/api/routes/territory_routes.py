from flask import Blueprint, request, jsonify
from services.territory_service import TerritoryService
from utils import not_found_if_none

territory_bp = Blueprint('territories', __name__)

@territory_bp.route('', methods=['POST'])
def create_territory():
    data = request.get_json()
    territory = TerritoryService.create_territory(data.get('name'), data.get('country-region-code'), data.get('group'))
    return jsonify(territory.to_dict()), 201

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
    territory = TerritoryService.update_territory(territory_id, data.get('name'), data.get('country-region-code'), data.get('group'))
    if not territory:
        return jsonify({"error": "Sales territory not found"}), 404
    return jsonify(territory.to_dict()), 200

@territory_bp.route('/<int:territory_id>', methods=['DELETE'])
def delete_territory(territory_id):
    success = TerritoryService.delete_territory(territory_id)
    if not success:
        return jsonify({"error": "Sales territory not found"}), 404
    return jsonify({"message": "Sales territory deleted"}), 200