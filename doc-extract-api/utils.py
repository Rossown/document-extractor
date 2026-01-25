from functools import wraps
from config import logger
from flask import jsonify

def not_found_if_none(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(result.to_dict()), 200
    return wrapper