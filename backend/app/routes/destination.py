from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.models import Destination
from app.helpers.helpers import model_to_dict
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
destination_bp = Blueprint('destination', __name__, url_prefix='/destination')


@destination_bp.route('/add', methods=['POST'])
@login_required
def add_destination():
    """Adds destination to database"""

    data = request.get_json()
    return create_entry(Destination, data, user_id=current_user.id)


@destination_bp.route('/get_all', methods=['GET'])
@login_required
def get_destinations():
    """Gets all destinations of user"""

    return get_paginated_entries(
        model=Destination,
        filters={'user_id': str(current_user.id)},
        order_by=Destination.position,
        model_key='destinations'
    )


@destination_bp.route('/get/<string:destination_id>', methods=['GET'])
@login_required
def get_destination(destination_id):
    """Gets specific destination of user"""

    # Check existence and permission of destination
    entry = check_existence_and_permission(Destination, destination_id)
    if isinstance(entry, tuple):
        return entry

    return jsonify({'destination': model_to_dict(entry)}), 200


@destination_bp.route('/edit/<string:destination_id>', methods=['POST'])
@login_required
def edit_destination(destination_id):
    """Edits destination"""

    data = request.get_json() # Get data

    # Check existence and permission of destination
    entry = check_existence_and_permission(Destination, destination_id)
    if isinstance(entry, tuple):
        return entry

    # Edit destination
    return edit_entry(Destination, destination_id, data)


@destination_bp.route('/edit_notes/<string:destination_id>', methods=['POST'])
@login_required
def edit_notes(destination_id):
    """Edit notes of destination"""

    # Get data
    data = request.get_json()
    free_text = data.get('free_text')

    # Check if data is given
    if free_text is None:
        return jsonify({'error': 'Note text is required'}), 400

    # Check existence and permission of destination
    entry = check_existence_and_permission(Destination, destination_id)
    if isinstance(entry, tuple):
        return entry

    # Update data
    return update_entry_field(Destination, destination_id, 'free_text', free_text)


@destination_bp.route('/reorder', methods=['POST'])
@login_required
def reorder_destinations():
    """Reorders destinations of user"""

    # Get new order from data
    data = request.get_json()
    new_order = data.get('new_order')

    # Reorder destinations
    return reorder_entries(Destination, {'user_id': current_user.id}, new_order, 'destinations')


@destination_bp.route('/delete/<string:destination_id>', methods=['DELETE'])
@login_required
def delete_destination(destination_id):
    """Deletes specific destination"""

    # Check existence and permission of destination
    entry = check_existence_and_permission(Destination, destination_id)
    if isinstance(entry, tuple):
        return entry

    # Delete destination
    return delete_entry(Destination, destination_id)

