from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from database import create_database_if_not_exists
from api.routes import api
from api.models import db

app = Flask(__name__)

# Database configuration
app.config.from_object(Config)

# Import models
db.init_app(app)

# Initialize the database
create_database_if_not_exists()
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(api, url_prefix='/api')