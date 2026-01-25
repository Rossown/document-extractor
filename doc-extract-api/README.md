# Document Extractor API

Flask REST API with PostgreSQL, SQLAlchemy ORM, and external API integration.

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure `.env`**
   ```env
   DB_CONN_STRING=postgresql://username:password@localhost:5432/doc_extract_api_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=doc_extract_api_db
   API_TIMEOUT=10
   API_RETRIES=3
   ```

3. **Run the app**
   ```bash
   flask run
   ```

## Structure
```
api/                    # Routes and models
  ├── routes.py
  └── models.py
services/               # Business logic
config.py              # Global config and logger
database.py            # DB initialization
app.py                 # Flask app entry point
```
## Logging

Logs include: timestamp, level, file:line, function name, message

Example:
```
2026-01-24 14:32:15 | INFO     | routes.py:10 | example_endpoint() | GET /example called
```

## Database Commands

```bash
# Connect
psql -U postgres -d doc_extract_api_db

# List tables
\dt

# Describe table
\d table_name
```

## Add New Endpoints

Edit `api/routes.py`:
```python
@api.route('/new', methods=['GET'])
def new_endpoint():
    return jsonify({'message': 'success'})
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