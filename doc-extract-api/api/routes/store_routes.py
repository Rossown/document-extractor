from flask import Blueprint, abort, request, jsonify
from services.store_service import StoreService
from utils import not_found_if_none

store_bp = Blueprint('stores', __name__)

@store_bp.route('', methods=['POST'])
def create_store():
    data = request.json
    store = StoreService.create_store(data['name'], {...})
    return jsonify({'id': store.id}), 201

@store_bp.route('', methods=['GET'])
def list_stores():
    return StoreService.list_stores()
    
@store_bp.route('/<int:store_id>', methods=['GET'])
@not_found_if_none
def get_store(store_id):
    return StoreService.get_store(store_id)
