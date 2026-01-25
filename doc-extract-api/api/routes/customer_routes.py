from flask import Blueprint, request, jsonify
from services.customer_service import CustomerService

customer_bp = Blueprint('customers', __name__)


@customer_bp.route('', methods=['POST'])
def create_customer():
    data = request.get_json()
    result = CustomerService.create_customer(**data)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    if result is None:
        return jsonify({"error": "Failed to create customer"}), 400
    return jsonify(result.to_dict()), 201

@customer_bp.route('', methods=['GET'])
def list_customers():
    customers = CustomerService.list_customers()
    return jsonify([c.to_dict() for c in customers])

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = CustomerService.get_customer_by_id(customer_id)
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer.to_dict())


@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    result = CustomerService.update_customer(customer_id, **data)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    if result is None:
        return jsonify({"error": "Failed to update customer"}), 400
    return jsonify(result.to_dict())

@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    success = CustomerService.delete_customer(customer_id)
    if not success:
        return jsonify({"error": "Failed to delete customer"}), 400
    return jsonify({"message": "Customer deleted successfully"}), 200