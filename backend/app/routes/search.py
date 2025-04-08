from flask import Blueprint, request, jsonify
from flask_login import login_required

from backend.app.models import Destination, Activity
from backend.app.helpers.helpers import search_resources

search_bp = Blueprint('search', __name__)


@search_bp.route('/search', methods=['GET'])
@login_required
def search():
    """Searches through strings in destinations and/or activities of user"""

    # Get query and type of entry
    query = request.args.get('query')
    type = request.args.get('type')

    # Check if search query exists
    if not query:
        return jsonify({'error': 'Search query required'}), 400

    # Set types of models that can be searched through
    types = ['destination', 'activity', 'both']

    # Set empty list for results
    results_data = []

    # Search through destinations
    if type == 'destination' or type == 'both' or type not in types:
        results_data.extend(search_resources(Destination, query))

    # Search through activities
    if type == 'activity' or type == 'both' or type not in types:
        results_data.extend(search_resources(Activity, query))

    return jsonify(results=results_data), 200

