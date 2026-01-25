from flask import Blueprint, abort, request, jsonify
from services.store_service import StoreService
from utils import not_found_if_none

store_bp = Blueprint('stores', __name__)

@store_bp.route('', methods=['POST'])
def create_store():
    data = request.get_json()
    address_data = {
        "address_type": data.get("address_type"),
        "address_line1": data.get("address_line1"),
        "address_line2": data.get("address_line2"),
        "city": data.get("city"),
        "state_province": data.get("state_province"),
        "postal_code": data.get("postal_code"),
        "country_region": data.get("country_region"),
    }
    store = StoreService.create_store(data['name'], address_data)
    return jsonify({'id': store.id}), 201

@store_bp.route('', methods=['GET'])
@not_found_if_none
def list_stores():
    return StoreService.list_stores()
    
@store_bp.route('/<int:store_id>', methods=['GET'])
@not_found_if_none
def get_store(store_id):
    return StoreService.get_store(store_id)

@store_bp.route('/<int:store_id>', methods=['PUT'])
def update_store(store_id):
    data = request.get_json()
    try:
        success = StoreService.update_store(store_id, **data)
        if not success:
            return jsonify({"error": "Store not found"}), 404
        return jsonify({"message": "Store updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@store_bp.route('/<int:store_id>', methods=['DELETE'])
def delete_store(store_id):
    try:
        success = StoreService.delete_store(store_id)
        if not success:
            return jsonify({"error": "Store not found"}), 404
        return jsonify({"message": "Store deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500