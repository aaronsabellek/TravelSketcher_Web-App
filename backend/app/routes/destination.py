from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.models import Destination
from app.routes.helpers.helpers import models_to_list
from app.routes.helpers.helpers_entries import (
    check_existence_and_permission,
    create_entry,
    edit_entry,
    delete_item,
    get_entry,
    reorder_items
)


# Set blueprint
destination_bp = Blueprint('destination', __name__, url_prefix='/destination')

# Add destination route
@destination_bp.route('/add', methods=['POST'])
@login_required
def add_destination():

    data = request.get_json()
    return create_entry(Destination, data, user_id=current_user.id)

# Get all destinations route
@destination_bp.route('/get_all', methods=['GET'])
@login_required
def get_destinations():

    destinations = Destination.query.filter_by(user_id=current_user.id).all()
    return jsonify(models_to_list(destinations))

# Get specific destination route
@destination_bp.route('/get/<int:destination_id>', methods=['GET'])
@login_required
def get_destination(destination_id):

    entry, status_code = get_entry(Destination, destination_id, current_user.id)
    return jsonify(entry), status_code

# Edit destination route
@destination_bp.route('/edit/<int:destination_id>', methods=['POST'])
@login_required
def edit_destination(destination_id):

    data = request.get_json() # Get data

    # Check for required title
    if not data.get('title') or data['title'] == '':
            return jsonify({'error': 'Title is required'}), 400

    # Check existence and permission of destination
    entry = check_existence_and_permission(Destination, destination_id, current_user.id)
    if isinstance(entry, tuple):
        return entry

    return edit_entry(Destination, destination_id, data, user_id=current_user.id)

# Reorder destinations route
@destination_bp.route('/reorder', methods=['POST'])
@login_required
def reorder_destinations():

    # Get new order from data
    data = request.get_json()
    new_order = data.get('new_order')

    return reorder_items(Destination, {'user_id': current_user.id}, new_order, 'destinations')

# Delete destination route
@destination_bp.route('/delete/<int:destination_id>', methods=['DELETE'])
@login_required
def delete_destination(destination_id):

    # Get destination
    destination = Destination.query.filter_by(id=destination_id, user_id=current_user.id).first()

    # Check if destination exists
    if not destination:
        return jsonify({'error': 'Destination not found or not permitted'}), 403

    return delete_item(Destination, destination_id)

