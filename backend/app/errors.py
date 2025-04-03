from flask import jsonify, current_app


def page_not_found(e):
    return jsonify({'error': 'Page not found', 'details': str(e)}), 404


def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed', 'details': str(e)}), 405


def handle_exception(e):
    """Handle global errors"""

    current_app.logger.error(f"Unexpected error: {str(e)}")
    return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


def handle_http_exception(e):
    """Handle HTTP errors"""

    current_app.logger.warning(f"{e.name} error occured: {e.description}")
    return jsonify({'error': e.name, 'details': e.description}), e.code


def handle_db_error(e):
    """HAndle database errors"""

    current_app.logger.error(f"Database error: {str(e)}")
    return jsonify({'error': 'A database error occurred', 'details': str(e)}), 500


