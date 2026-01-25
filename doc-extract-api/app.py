from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from utils import create_database_if_not_exists
from api.routes import api
from api.models import db
from api.error_handlers import register_error_handlers
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Database configuration
app.config.from_object(Config)

# Initialize the database (do not call db.create_all() when using migrations)
create_database_if_not_exists()

# Import models and initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Register error handlers
register_error_handlers(app)

# Register blueprints
app.register_blueprint(api, url_prefix='/api')