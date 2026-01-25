import os
import psycopg2
from functools import wraps
from config import logger
from flask import jsonify
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql

def not_found_if_none(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return jsonify({'error': 'Not found'}), 404
        if isinstance(result, list):
            return jsonify([item.to_dict() for item in result]), 200
        if hasattr(result, 'to_dict'):
            return jsonify(result.to_dict()), 200
        return jsonify(result), 200
    return wrapper

def create_database_if_not_exists():
    """
    Create the PostgreSQL database if it does not exist.
    """
    # Get database connection parameters from environment variables
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    # Connect to PostgreSQL server
    conn = psycopg2.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    try:
        # Check if database exists and create it if not
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        logger.info(f"Database {db_name} created successfully.")
    except psycopg2.Error as e:
        if 'already exists' in str(e):
            logger.info(f"Database {db_name} already exists.")
        else:
            logger.error(f"Error creating database: {e}")
            raise
    finally:
        cur.close()
        conn.close()