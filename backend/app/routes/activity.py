import re
from flask import Blueprint, request, jsonify
from flask_login import login_required

from app.models import Destination, Activity
from app.helpers.helpers import model_to_dict, is_valid_url
from app.helpers.helpers_entries import (
    check_existence_and_permission,
    create_entry,
    get_paginated_entries,
    edit_entry,
    update_entry_field,
    reorder_entries,
    delete_entry
)

# Set blueprint
activity_bp = Blueprint('activity', __name__, url_prefix='/activity')


@activity_bp.route('/add/<string:destination_id>', methods=['POST'])
@login_required
def add_activity(destination_id):
    """Adds activity to database"""

    data = request.get_json() # Get data

    # Check if destination of activity exists and belongs to user
    destination = check_existence_and_permission(Destination, destination_id)
    if isinstance(destination, tuple):
        return destination

    # Create activity
    return create_entry(Activity, data, destination_id=destination_id)


@activity_bp.route('/get_all/<string:destination_id>', methods=['GET'])
@login_required
def get_activities(destination_id):
    """Gets all activities for a destination with pagination"""

    # Check existence and permission of destination
    entry = check_existence_and_permission(Destination, destination_id)
    if isinstance(entry, tuple):
        return entry

    # Get destination by id
    destination = Destination.query.filter_by(id=destination_id).first()

    return get_paginated_entries(
        model=Activity,
        filters={'destination_id': destination_id},
        order_by=Activity.position,
        model_key='activities',
        extra_data={
            'destination': destination.title,
            'country': destination.country
        }
    )


@activity_bp.route('/get/<string:activity_id>', methods=['GET'])
@login_required
def get_activity(activity_id):
    """Gets specific destination of user"""

    # Check existence and permission of activity
    entry = check_existence_and_permission(Activity, activity_id)
    if isinstance(entry, tuple):
        return entry

    return jsonify({'activity': model_to_dict(entry)}), 200


@activity_bp.route('/edit/<string:activity_id>', methods=['POST'])
@login_required
def edit_activity(activity_id):
    """Edits activity"""

    data = request.get_json() # Get data

    # Check existence and permission of activity
    entry = check_existence_and_permission(Activity, activity_id)
    if isinstance(entry, tuple):
        return entry

    # Edit activity
    return edit_entry(Activity, activity_id, data)


@activity_bp.route('/edit_link/<string:activity_id>', methods=['POST'])
@login_required
def edit_link(activity_id):
    """Edit weblink of activity"""

    # Get data
    data = request.get_json()
    web_link = data.get('web_link')

    # Check if data is given
    if web_link == '':
        return jsonify({'error': 'Web link is required'}), 400

    # Check if link has correct web link format
    if not is_valid_url(web_link):
        return jsonify({'error': 'Input is no web link format'}), 400

    # Check existence and permission of activity
    entry = check_existence_and_permission(Activity, activity_id)
    if isinstance(entry, tuple):
        return entry

    # Update data
    return update_entry_field(Activity, activity_id, 'web_link', web_link)


@activity_bp.route('/edit_notes/<string:activity_id>', methods=['POST'])
@login_required
def edit_notes(activity_id):
    """Edit notes of activity"""

    # Get data
    data = request.get_json()
    free_text = data.get('free_text')

    # Check if data is given
    if free_text == '':
        return jsonify({'error': 'Note text is required'}), 400

    # Check existence and permission of activity
    entry = check_existence_and_permission(Activity, activity_id)
    if isinstance(entry, tuple):
        return entry

    # Update data
    return update_entry_field(Activity, activity_id, 'free_text', free_text)


@activity_bp.route('/reorder/<string:destination_id>', methods=['POST'])
@login_required
def reorder_activities(destination_id):
    """Reorders activities of specific destination"""

    # Check existence and permission of activity
    entry = check_existence_and_permission(Destination, destination_id)
    if isinstance(entry, tuple):
        return entry

    # Get new order from data
    data = request.get_json()
    new_order = data.get('new_order')

    # Reorder destinations
    return reorder_entries(Activity, {'destination_id': destination_id}, new_order, 'activities')


@activity_bp.route('/delete/<string:activity_id>', methods=['DELETE'])
@login_required
def delete_activity(activity_id):
    """Deletes activity from database"""

    # Check existence and permission of activity
    entry = check_existence_and_permission(Activity, activity_id)
    if isinstance(entry, tuple):
        return entry

    # Delete activity
    return delete_entry(Activity, activity_id)

