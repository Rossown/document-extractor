from flask import Blueprint, request, jsonify
from services.sales_order_service import SalesOrderService
from utils import not_found_if_none

sales_order_bp = Blueprint('sales-orders', __name__)

@sales_order_bp.route('', methods=['POST'])
def create_sales_order():
    data = request.get_json()
    header = data.get('header')
    details = data.get('details', [])
    try:
        order = SalesOrderService.create_sales_order(header, details)
        return jsonify({
            "id": order.id,
            "sales_order_number": order.sales_order_number,
            "header": {
                "customer_id": order.customer_id,
                "order_date": order.order_date,
                "status": order.status
            },
            "details": [
                {
                    "id": detail.id,
                    "product_id": detail.product_id,
                    "quantity": detail.quantity,
                    "unit_price": detail.unit_price
                } for detail in order.sales_order_details
            ]
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@sales_order_bp.route('', methods=['GET'])
@not_found_if_none
def list_sales_orders():
    return SalesOrderService.list_sales_orders()

@sales_order_bp.route('/<int:order_id>', methods=['GET'])
@not_found_if_none
def get_sales_order(order_id):
    return SalesOrderService.get_sales_order_by_id(order_id)
    

@sales_order_bp.route('/<int:order_id>', methods=['PUT'])
def update_sales_order(order_id):
    data = request.get_json()
    try:
        success = SalesOrderService.update_sales_order(order_id, **data)
        if not success:
            return jsonify({"error": "Sales order not found"}), 404
        return jsonify({"message": "Sales order updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sales_order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_sales_order(order_id):
    try:
        success = SalesOrderService.delete_sales_order(order_id)
        if not success:
            return jsonify({"error": "Sales order not found"}), 404
        return jsonify({"message": "Sales order deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@sales_order_bp.route('/<int:order_id>/details', methods=['GET'])
@not_found_if_none
def list_sales_order_details(order_id):
    return SalesOrderService.get_sales_order_details(order_id)

@sales_order_bp.route('/<int:order_id>/details/<int:detail_id>', methods=['GET'])
@not_found_if_none
def get_sales_order_detail(order_id, detail_id):
    return SalesOrderService.get_sales_order_detail_by_id(order_id, detail_id)