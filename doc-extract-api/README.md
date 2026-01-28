
# Document Extractor API

This project is a modular Flask REST API for document and sales data management, using PostgreSQL and SQLAlchemy ORM. It supports:

- CRUD operations for Products, Categories, Subcategories, Stores, Customers, Sales Orders, and more
- Polymorphic address support for sales orders (person or store)
- Relationship-aware endpoints (e.g., products include subcategory and category info)
- Robust error handling for unique and foreign key constraints
- Consistent JSON serialization for all endpoints
- External API and AI integration for document extraction

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure `.env`**
   ```env
   DB_CONN_STRING=postgresql://username:password@db:5432/doc_extract_api_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=db
   DB_PORT=5432
   DB_NAME=doc_extract_api_db
   API_TIMEOUT=10
   API_RETRIES=3
   OPENAI_API_KEY=
   ```

3. **Run the app**
   ```bash
   flask run
   ```

## Structure
```
api/                      # API layer
   ├── routes/             # All Flask route blueprints (one per resource)
   └── models.py           # SQLAlchemy models
services/                 # Business logic for each resource
```
## Logging

Logs include: timestamp, level, file:line, function name, message

Example:
```
2026-01-24 14:32:15 | INFO     | routes.py:10 | example_endpoint() | GET /example called
```

## Add New Endpoints

Create `api/routes/new_service_routes.py`
Edit `api/routes/new_service_routes.py`:
```python
from flask import Blueprint, jsonify
from services.new_service import NewService
from utils import not_found_if_none

new_service_bp = Blueprint('new-service', __name__)
@api.route('/new', methods=['GET'])
def new_endpoint():
    return jsonify({'message': 'success'})
```

Edit `api/routes/__init__.py`:
```python
from .new_service_routes import new_service_bp
...
api.register_blueprint(new_service_bp, url_prefix='/new-service')
```

## Add New Models

Edit `api/models.py`:
```python
class NewModel(db.Model):
    __tablename__ = 'new_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
```

Database and Tables auto-create on startup.