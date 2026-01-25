from flask import jsonify
from api.errors import AppError
from config import logger

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
