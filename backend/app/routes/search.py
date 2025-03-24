from flask import Blueprint, request, jsonify
from flask_login import login_required

from app.models import Destination, Activity
from app.routes.helpers import search_resources

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
@login_required
def search():
    search_query = request.args.get('search_query')  # Der Suchtext
    resource_type = request.args.get('resource_type')  # 'destination', 'activity' oder 'both' für beide

    if not search_query:
        return jsonify({'error': 'Suchtext ist erforderlich'}), 400

    # Felder, die wir nicht durchsuchen wollen (ID, Position und Beziehungen)
    exclude_fields = ['id', 'position', 'user_id', 'destination_id']  # Anpassbar je nach Bedarf

    results_data = []

    # Wenn nur 'destination' angegeben ist
    if resource_type == 'destination' or resource_type == 'both' or not resource_type:
        results_data.extend(search_resources(Destination, search_query, exclude_fields))

    # Wenn nur 'activity' angegeben ist
    if resource_type == 'activity' or resource_type == 'both' or not resource_type:
        results_data.extend(search_resources(Activity, search_query, exclude_fields))

    return jsonify(results=results_data), 200

