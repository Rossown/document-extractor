from flask import Blueprint, abort, request, jsonify
from services.store_service import StoreService

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
    return jsonify(store.to_dict()), 201

@store_bp.route('', methods=['GET'])
def list_stores():
    cursor = request.args.get('cursor', type=int)
    limit = request.args.get('limit', type=int, default=20)
    stores = StoreService.list_stores(cursor_id=cursor, limit=limit)
    return jsonify(stores), 200

@store_bp.route('/<int:store_id>', methods=['GET'])
def get_store(store_id):
    store = StoreService.get_store(store_id)
    return jsonify(store.to_dict()), 200

@store_bp.route('/<int:store_id>', methods=['PUT'])
def update_store(store_id):
    data = request.get_json()
    data.pop("id", None)
    store = StoreService.update_store(store_id, **data)
    return jsonify(store.to_dict()), 200

@store_bp.route('/<int:store_id>', methods=['DELETE'])
def delete_store(store_id):
    StoreService.delete_store(store_id)
    return jsonify({"message": "Store deleted successfully"}), 204
