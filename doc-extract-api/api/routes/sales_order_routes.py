from flask import Blueprint, request, jsonify
from services.sales_order_service import SalesOrderService

sales_order_bp = Blueprint('sales-orders', __name__)

@sales_order_bp.route('', methods=['POST'])
def create_sales_order():
    data = request.get_json()
    header = data.get('header')
    details = data.get('details', [])
    order = SalesOrderService.create_sales_order(header, details)
    return jsonify(order.to_dict()), 201
    
@sales_order_bp.route('', methods=['GET'])
def list_sales_orders():
    cursor = request.args.get('cursor', type=int)
    limit = request.args.get('limit', type=int, default=20)
    orders = SalesOrderService.list_sales_orders(cursor_id=cursor, limit=limit)
    return jsonify([o.to_dict() for o in orders]), 200

@sales_order_bp.route('/<int:order_id>', methods=['GET'])
def get_sales_order(order_id):
    order = SalesOrderService.get_sales_order_by_id(order_id)
    return jsonify(order.to_dict()), 200
    

@sales_order_bp.route('/<int:order_id>', methods=['PUT'])
def update_sales_order(order_id):
    data = request.get_json()
    order = SalesOrderService.update_sales_order(order_id, **data)
    return jsonify(order.to_dict()), 200

@sales_order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_sales_order(order_id):
    SalesOrderService.delete_sales_order(order_id)
    return jsonify({"message": "Sales order deleted successfully"}), 204

# Sales Order Details
@sales_order_bp.route('/<int:order_id>/details', methods=['POST'])
def add_sales_order_detail(order_id):
    data = request.get_json()
    detail = SalesOrderService.add_sales_order_detail(order_id, data)
    return jsonify(detail.to_dict()), 201

@sales_order_bp.route('/<int:order_id>/details', methods=['GET'])
def list_sales_order_details(order_id):
    cursor = request.args.get('cursor', type=int)
    limit = request.args.get('limit', type=int, default=20)
    details = SalesOrderService.get_sales_order_details(order_id)
    return jsonify([d.to_dict() for d in details])

@sales_order_bp.route('/<int:order_id>/details/<int:detail_id>', methods=['GET'])
def get_sales_order_detail(order_id, detail_id):
    detail = SalesOrderService.get_sales_order_detail_by_id(order_id, detail_id)
    if detail is None:
        return jsonify({"error": "Sales order detail not found"}), 404
    return jsonify(detail.to_dict())


@sales_order_bp.route('/<int:order_id>/details/<int:detail_id>', methods=['PUT'])
def update_sales_order_detail(order_id, detail_id):
    data = request.get_json()
    detail = SalesOrderService.update_sales_order_detail(order_id, detail_id, **data)
    return jsonify(detail.to_dict()), 200

@sales_order_bp.route('/<int:order_id>/details/<int:detail_id>', methods=['DELETE'])
def delete_sales_order_detail(order_id, detail_id):
    SalesOrderService.delete_sales_order_detail(order_id, detail_id)
    return jsonify({"message": "Sales order detail deleted successfully"}), 204