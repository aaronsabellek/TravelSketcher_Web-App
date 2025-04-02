from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.models import Destination, Activity
from app.routes.helpers.helpers import models_to_list
from app.routes.helpers.helpers_entries import (
    create_entry,
    get_entry,
    edit_entry,
    reorder_items,
    delete_item
)


# Set blueprint
activity_bp = Blueprint('activity', __name__, url_prefix='/activity')

@activity_bp.route('/add', methods=['POST'])
@login_required
def add_activity():
    data = request.get_json()
    destination_id = data.get('destination_id')

    if not Destination.query.get(destination_id):
        return jsonify({'error': 'Destination not found'}), 404

    return create_entry(Activity, data, destination_id=destination_id)

@activity_bp.route('/get_activities/<int:destination_id>', methods=['GET'])
@login_required
def get_activities(destination_id):

    destination = Destination.query.get(destination_id)

    if not destination:
        return jsonify({'error': 'Destination not found'}), 404

    # Überprüfen, ob der aktuelle Benutzer der Besitzer der Destination ist
    if destination.user_id != current_user.id:
        return jsonify({'error': 'Keine Berechtigung für diese Destination'}), 403

    activities = Activity.query.filter_by(destination_id=destination_id).all()

    return jsonify({
        'destination': destination.title,
        'activities': models_to_list(activities)  # Kein manuelles Mapping mehr nötig!
    })

@activity_bp.route('/get/<int:activity_id>', methods=['GET'])
@login_required
def get_activity(activity_id):
    # Benutze die Hilfsfunktion, um die Activity-Daten zu holen
    activity_data, status_code = get_entry(Activity, activity_id)

    if status_code != 200:
        return jsonify({'error': 'Activity nicht gefunden'}), status_code

    # Sicherstellen, dass der Benutzer Zugriff auf die Activity hat
    activity = Activity.query.get(activity_id)
    if activity.destination.owner.id != current_user.id:
        return jsonify({'error': 'Nicht autorisiert'}), 403

    return jsonify(activity_data), status_code

@activity_bp.route('/edit/<int:activity_id>', methods=['POST'])
@login_required
def edit_activity(activity_id):
    data = request.get_json()
    activity = Activity.query.get(activity_id)

    # Stelle sicher, dass der Nutzer berechtigt ist, die Activity zu bearbeiten
    if activity.destination.owner.id != current_user.id:
        return jsonify({'error': 'Nicht autorisiert'}), 403

    return edit_entry(Activity, activity_id, data)

@activity_bp.route('/reorder/<int:destination_id>', methods=['POST'])
@login_required
def reorder_activities(destination_id):
    data = request.get_json()
    new_order = data.get("activities")
    return reorder_items(Activity, {"destination_id": destination_id}, new_order, "activities")

@activity_bp.route('/delete/<int:activity_id>', methods=['DELETE'])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get(activity_id)

    if activity is None:
        return jsonify({'error': 'Activity not found'}), 404

    # Prüfen, ob der aktuelle Benutzer der Besitzer der zugehörigen Destination ist
    if activity.destination.user_id != current_user.id:
        return jsonify({'error': 'You are not authorized to delete this activity'}), 403

    return delete_item(Activity, activity_id)

