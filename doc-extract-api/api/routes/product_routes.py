from flask import Blueprint, request, jsonify
from services.product_service import ProductService
from utils import not_found_if_none

product_bp = Blueprint('products', __name__)

# ProductData
@product_bp.route('', methods=['GET'])
@not_found_if_none
def list_products():
    return ProductService.list_products()

@product_bp.route('/<int:product_id>', methods=['GET'])
@not_found_if_none
def get_product(product_id):
    return ProductService.get_product_by_id(product_id)

@product_bp.route('', methods=['POST'])
def create_product():
    data = request.get_json()
    result = ProductService.create_product(data)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    if result is None:
        return jsonify({"error": "Failed to create product"}), 400
    return jsonify(result.to_dict()), 201

@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    result = ProductService.update_product(product_id, data)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    if result is None:
        return jsonify({"error": "Failed to update product"}), 400
    return jsonify(result.to_dict()), 200

@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    success = ProductService.delete_product(product_id)
    if not success:
        return jsonify({"error": "Failed to delete product"}), 400
    return jsonify({"message": "Product deleted successfully"}), 200

# ProductSubCategory Routes

@product_bp.route('/subcategories', methods=['GET'])
@not_found_if_none
def list_product_subcategories():
    return ProductService.list_subcategories()

@product_bp.route('/subcategories/<int:subcategory_id>', methods=['GET'])
@not_found_if_none
def get_product_subcategory(subcategory_id):
    return ProductService.get_subcategory_by_id(subcategory_id)

@product_bp.route('/subcategories', methods=['POST'])
def create_product_subcategory():
    data = request.get_json()
    result = ProductService.create_subcategory(data)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    if result is None:
        return jsonify({"error": "Failed to create product subcategory"}), 400
    return jsonify(result.to_dict()), 201

@product_bp.route('/subcategories/<int:subcategory_id>', methods=['PUT'])
def update_product_subcategory(subcategory_id):
    data = request.get_json()
    result = ProductService.update_subcategory(subcategory_id, data)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    if result is None:
        return jsonify({"error": "Failed to update product subcategory"}), 400
    return jsonify(result.to_dict()), 200

@product_bp.route('/subcategories/<int:subcategory_id>', methods=['DELETE'])
def delete_product_subcategory(subcategory_id):
    success = ProductService.delete_subcategory(subcategory_id)
    if not success:
        return jsonify({"error": "Failed to delete product subcategory"}), 400
    return jsonify({"message": "Product subcategory deleted successfully"}), 200

# ProductCategory Routes

@product_bp.route('/categories', methods=['GET'])
@not_found_if_none
def list_product_categories():
    return ProductService.list_categories()

@product_bp.route('/categories/<int:category_id>', methods=['GET'])
@not_found_if_none
def get_product_category(category_id):
    return ProductService.get_category_by_id(category_id)

@product_bp.route('/categories', methods=['POST'])
def create_product_category():
    data = request.get_json()
    result = ProductService.create_category(data)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    if result is None:
        return jsonify({"error": "Failed to create product category"}), 400
    return jsonify(result.to_dict()), 201

@product_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_product_category(category_id):
    data = request.get_json()
    result = ProductService.update_category(category_id, data)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    if result is None:
        return jsonify({"error": "Failed to update product category"}), 400
    return jsonify(result.to_dict()), 200

@product_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_product_category(category_id):
    success = ProductService.delete_category(category_id)
    if not success:
        return jsonify({"error": "Failed to delete product category"}), 400
    return jsonify({"message": "Product category deleted successfully"}), 200