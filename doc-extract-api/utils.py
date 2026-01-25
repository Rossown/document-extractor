import os
import psycopg2
from functools import wraps
from config import logger
from flask import jsonify
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql


def paginate(query, cursor_id=None, limit=20, order_by=None):
    """
    Cursor-based pagination for SQLAlchemy queries.

    :param query: SQLAlchemy query object
    :param cursor_id: the ID (or key) to start after
    :param limit: max number of items to return
    :param order_by: column to order by (SQLAlchemy column object)
    :return: dict with items and next_cursor
    """
    # Determine default order column if none provided
    if order_by is None:
        model = query.column_descriptions[0]['entity']
        if model is None:
            raise ValueError("Cannot determine model from query, provide 'order_by'")
        order_by = model.id  # assumes primary key column is named 'id'

    # Apply ordering
    query = query.order_by(order_by)

    # Apply cursor filter
    if cursor_id is not None:
        query = query.filter(order_by > cursor_id)

    # Fetch limited results
    items = query.limit(limit).all()

    # Determine next cursor
    next_cursor = getattr(items[-1], order_by.key) if items else None

    return {
        "items": [item.to_dict() for item in items],
        "next_cursor": next_cursor,
        "limit": limit,
        "count": len(items)
    }


    
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