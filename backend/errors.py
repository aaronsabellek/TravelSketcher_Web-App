from flask import jsonify


# Global errors
def handle_exception(e):
    return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# HTTP errors
def handle_http_exception(e):
    return jsonify({'error': e.name, 'details': e.description}), e.code

# DB errors
def handle_db_error(e):
    return jsonify({'error': 'A database error occurred', 'details': str(e)}), 500
