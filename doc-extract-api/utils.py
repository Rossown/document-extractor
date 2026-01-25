import os
import psycopg2
from functools import wraps
from config import logger
from flask import jsonify
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql

def paginate(query, *, order_by, cursor_id=None, limit=20):
    """
    Cursor-based pagination for SQLAlchemy queries.

    :param query: SQLAlchemy Query
    :param order_by: SQLAlchemy column (REQUIRED)
    :param cursor_id: last seen value
    :param limit: page size
    """

    if order_by is None:
        raise ValueError("paginate() requires an explicit order_by column")

    # Always deterministic ordering
    query = query.order_by(order_by.asc())

    # Cursor filter (exclusive)
    if cursor_id is not None:
        query = query.filter(order_by > cursor_id)

    # Fetch one extra row to detect next page
    results = query.limit(limit + 1).all()

    next_cursor = None
    if len(results) > limit:
        next_cursor = getattr(results[limit - 1], order_by.key)
        results = results[:limit]
        

    return {
        "items": [item.to_dict() for item in results],
        "next_cursor": next_cursor,
        "limit": limit,
        "count": len(results),
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