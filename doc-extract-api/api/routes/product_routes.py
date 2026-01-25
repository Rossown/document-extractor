from flask import Blueprint, request, jsonify
from services.product_service import ProductService

product_bp = Blueprint('products', __name__)

# ProductData
@product_bp.route('', methods=['POST'])
def create_product():
    data = request.get_json()
    result = ProductService.create_product(data)
    return jsonify(result.to_dict()), 201

@product_bp.route('', methods=['GET'])
def list_products():
    products = ProductService.list_products()
    return jsonify(products)

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductService.get_product_by_id(product_id)
    return jsonify(product), 200


@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    result = ProductService.update_product(product_id, data)
    return jsonify(result.to_dict()), 200

@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    ProductService.delete_product(product_id)
    return jsonify({"message": "Product deleted successfully"}), 204

# ProductSubCategory Routes
@product_bp.route('/subcategories', methods=['POST'])
def create_product_subcategory():
    data = request.get_json()
    result = ProductService.create_subcategory(data)
    return jsonify(result.to_dict()), 201

@product_bp.route('/subcategories', methods=['GET'])
def list_product_subcategories():
    subcategories = ProductService.list_subcategories()
    return jsonify([s.to_dict() for s in subcategories])

@product_bp.route('/subcategories/<int:subcategory_id>', methods=['GET'])
def get_product_subcategory(subcategory_id):
    subcategory = ProductService.get_subcategory_by_id(subcategory_id)
    return jsonify(subcategory.to_dict())


@product_bp.route('/subcategories/<int:subcategory_id>', methods=['PUT'])
def update_product_subcategory(subcategory_id):
    data = request.get_json()
    result = ProductService.update_subcategory(subcategory_id, data)
    return jsonify(result.to_dict()), 200

@product_bp.route('/subcategories/<int:subcategory_id>', methods=['DELETE'])
def delete_product_subcategory(subcategory_id):
    ProductService.delete_subcategory(subcategory_id)
    return jsonify({"message": "Product subcategory deleted successfully"}), 204

# ProductCategory Routes
@product_bp.route('/categories', methods=['POST'])
def create_product_category():
    data = request.get_json()
    result = ProductService.create_category(data)
    return jsonify(result.to_dict()), 201

@product_bp.route('/categories', methods=['GET'])
def list_product_categories():
    products = ProductService.list_categories()
    return jsonify([p.to_dict() for p in products])

@product_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_product_category(category_id):
    category = ProductService.get_category_by_id(category_id)
    return jsonify(category.to_dict())


@product_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_product_category(category_id):
    data = request.get_json()
    result = ProductService.update_category(category_id, data)
    return jsonify(result.to_dict()), 200

@product_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_product_category(category_id):
    ProductService.delete_category(category_id)
    return jsonify({"message": "Product category deleted successfully"}), 204