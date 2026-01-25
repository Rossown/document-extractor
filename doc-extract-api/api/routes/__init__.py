from flask import Blueprint

# Create main API blueprint
api = Blueprint('api', __name__)

# Import all route modules
from .store_routes import store_bp
from .product_routes import product_bp
from .sales_order_routes import sales_order_bp
from .territory_routes import territory_bp
from .customer_routes import customer_bp
from .person_routes import person_bp
from .product_routes import product_bp

# Register sub-blueprints
api.register_blueprint(store_bp, url_prefix='/stores')
api.register_blueprint(product_bp, url_prefix='/products')
api.register_blueprint(sales_order_bp, url_prefix='/sales-orders')
api.register_blueprint(person_bp, url_prefix='/persons')
api.register_blueprint(customer_bp, url_prefix='/customers')
api.register_blueprint(territory_bp, url_prefix='/territories')