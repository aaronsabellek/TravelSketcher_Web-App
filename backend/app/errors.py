from flask import jsonify, current_app


# Global errors
def handle_exception(e):
    current_app.logger.error(f"Unexpected error: {str(e)}")
    return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# HTTP errors
def handle_http_exception(e):
    current_app.logger.warning(f"{e.name} error occured: {e.description}")
    return jsonify({'error': e.name, 'details': e.description}), e.code

# DB errors
def handle_db_error(e):
    current_app.logger.error(f"Database error: {str(e)}")
    return jsonify({'error': 'A database error occurred', 'details': str(e)}), 500
