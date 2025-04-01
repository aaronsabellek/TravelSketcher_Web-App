from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.models import Destination
from app.routes.helpers import (
    create_entry,
    edit_entry,
    delete_item,
    models_to_list,
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

    # Check if destination exists and belongs to user
    destination = Destination.query.filter_by(id=destination_id, user_id=current_user.id).first()
    if not destination:
        return jsonify({'error': 'Destination not found or not permitted'}), 403

    # Return relevant data
    return jsonify({key: getattr(destination, key) for key in Destination.__table__.columns.keys() if not key.startswith('_')}), 200

# Edit destination route
@destination_bp.route('/edit/<int:destination_id>', methods=['POST'])
@login_required
def edit_destination(destination_id):

    data = request.get_json() # Get data

    # Check if destination belongs to user
    destination = Destination.query.filter_by(id=destination_id, user_id=current_user.id).first()
    if not destination:
        return jsonify({'error': 'Destination not found or not permitted'}), 403

    return edit_entry(Destination, destination_id, data)

# Reorder destinations route
@destination_bp.route('/reorder', methods=['POST'])
@login_required
def reorder_destinations():

    # Get new order from data
    data = request.get_json()
    new_order = data.get('new_order')

    return reorder_items(Destination, {'user_id': current_user.id}, new_order, 'destinations')

@destination_bp.route('/delete/<int:destination_id>', methods=['DELETE'])
@login_required  # Damit der User eingeloggt sein muss
def delete_destination(destination_id):
    # Hole die Destination anhand der ID
    destination = Destination.query.filter_by(id=destination_id, user_id=current_user.id).first()

    # Wenn die Destination nicht existiert, gib einen Fehler zurück
    if destination is None:
        return jsonify({'error': 'Destination not found!'}), 404

    return delete_item(Destination, destination_id)

