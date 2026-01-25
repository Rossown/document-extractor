from flask import jsonify
from api.errors import AppError
from api.models import db
from config import logger
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(error):
        logger.error(error.message)
        return jsonify({
            "error": error.message
        }), error.status_code

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "error": "Endpoint not found"
        }), 404

    @app.errorhandler(500)
    def handle_500(error):
        logger.exception("Unhandled exception")
        return jsonify({
            "error": "Internal server error"
        }), 500
        

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(error):
        db.session.rollback()
        logger.exception("Database error")
        return jsonify({"error": "Database error"}), 500

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback()
        logger.exception("Integrity error")
        return jsonify({"error": "Integrity error"}), 409