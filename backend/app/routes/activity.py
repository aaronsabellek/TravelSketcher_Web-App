from flask import Blueprint, request, jsonify
from flask_login import login_required

from app.models import Destination, Activity
from app.helpers.helpers import models_to_list, model_to_dict
from app.helpers.helpers_entries import (
    check_existence_and_permission,
    create_entry,
    edit_entry,
    reorder_entries,
    delete_entry
)

# Set blueprint
activity_bp = Blueprint('activity', __name__, url_prefix='/activity')


@activity_bp.route('/add', methods=['POST'])
@login_required
def add_activity():
    """Adds activity to database"""

    data = request.get_json() # Get data

    # Check if destination of activity exists and belongs to user
    destination_id = data.get('destination_id')
    destination = check_existence_and_permission(Destination, destination_id)
    if isinstance(destination, tuple):
        return destination

    # Create activity
    return create_entry(Activity, data, destination_id=data.get('destination_id'))


@activity_bp.route('/get_all/<int:destination_id>', methods=['GET'])
@login_required
def get_activities(destination_id):
    """Get all destinations of user"""

    # Check existence and permission of activity
    entry = check_existence_and_permission(Destination, destination_id)
    if isinstance(entry, tuple):
        return entry

    # Set destination and activities
    destination = Destination.query.get(destination_id)
    activities = Activity.query.filter_by(destination_id=destination_id).all()

    # Check if activities of destination are empty
    if not activities:
        return jsonify({'activities': [], 'message': f"Destination '{destination.title}' has no activities yet"}), 200

    # Return activities
    return jsonify({
        'destination': destination.title,
        'activities': models_to_list(activities)
    })


@activity_bp.route('/get/<int:activity_id>', methods=['GET'])
@login_required
def get_activity(activity_id):
    """Get specific destination of user"""

    # Check existence and permission of activity
    entry = check_existence_and_permission(Activity, activity_id)
    if isinstance(entry, tuple):
        return entry

    # Return activity
    return jsonify({'activity': model_to_dict(entry)}), 200


@activity_bp.route('/edit/<int:activity_id>', methods=['POST'])
@login_required
def edit_activity(activity_id):
    """Edit activity in database"""

    data = request.get_json() # Get data

    # Check existence and permission of activity
    entry = check_existence_and_permission(Activity, activity_id)
    if isinstance(entry, tuple):
        return entry

    # Edit activity
    return edit_entry(Activity, activity_id, data)


@activity_bp.route('/reorder/<int:destination_id>', methods=['POST'])
@login_required
def reorder_activities(destination_id):
    """Reorder activities of specific destination"""

    # Check existence and permission of activity
    entry = check_existence_and_permission(Destination, destination_id)
    if isinstance(entry, tuple):
        return entry

    # Get new order from data
    data = request.get_json()
    new_order = data.get('new_order')

    # Reorder destinations
    return reorder_entries(Activity, {'destination_id': destination_id}, new_order, 'activities')


@activity_bp.route('/delete/<int:activity_id>', methods=['DELETE'])
@login_required
def delete_activity(activity_id):
    """Delete activity from database"""

    # Check existence and permission of activity
    entry = check_existence_and_permission(Activity, activity_id)
    if isinstance(entry, tuple):
        return entry

    # Delete activity
    return delete_entry(Activity, activity_id)

