from flask import Blueprint, request, jsonify
from services.customer_service import CustomerService

customer_bp = Blueprint('customers', __name__)


@customer_bp.route('', methods=['POST'])
def create_customer():
    data = request.get_json()
    result = CustomerService.create_customer(**data)
    return jsonify(result.to_dict()), 201

@customer_bp.route('', methods=['GET'])
def list_customers():
    cursor = request.args.get('cursor', type=int)
    limit = request.args.get('limit', type=int, default=20)
    customers = CustomerService.list_customers(cursor_id=cursor, limit=limit)
    return jsonify(customers), 200

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = CustomerService.get_customer_by_id(customer_id)
    return jsonify(customer.to_dict()), 200


@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    data.pop("id", None)
    result = CustomerService.update_customer(customer_id, **data)
    return jsonify(result.to_dict()), 200

@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    CustomerService.delete_customer(customer_id)
    return jsonify({"message": "Customer deleted successfully"}), 204