from flask import Blueprint

# Initialize the API blueprint
api = Blueprint('api', __name__)

# Import routes
from . import routes
