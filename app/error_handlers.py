from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Create handlers
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    console_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Log the error
        app.logger.error(f'Unhandled Exception: {str(e)}', exc_info=True)

        # Handle HTTP exceptions
        if isinstance(e, HTTPException):
            response = {
                'error': e.name,
                'message': e.description
            }
            return jsonify(response), e.code

        # Handle validation errors
        if isinstance(e, ValueError):
            response = {
                'error': 'Validation Error',
                'message': str(e)
            }
            return jsonify(response), 400

        # Handle other exceptions
        response = {
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }
        return jsonify(response), 500

    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f'Resource not found: {error}')
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(400)
    def bad_request_error(error):
        app.logger.warning(f'Bad request: {error}')
        return jsonify({'error': str(error)}), 400

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
