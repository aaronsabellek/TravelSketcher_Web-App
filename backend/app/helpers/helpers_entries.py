from flask import jsonify
from flask_login import logout_user

from app import db
from app.models import User, Destination, Activity
from app.helpers.helpers import model_to_dict


# Check existence and persmission of entry
def check_existence_and_permission(model, entry_id, user_id):

    # Check if entry exists
    entry = model.query.filter_by(id=entry_id).first()
    if not entry:
            return {'error': f'{model.__name__} not found'}, 404

    # Check permission of user
    entry = model.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return {'error': f'{model.__name__} not permitted'}, 403

    return entry

# Create entry
def create_entry(model, data, user_id=None, destination_id=None):

    # Get valid data as dict
    data = {key: value for key, value in data.items() if key in model.__table__.columns}

    # Check if required title exists
    if not data.get('title') or data['title'] == '':
        return jsonify({'error': 'Title is required'}), 400

    # Set query
    position_query = db.session.query(db.func.max(model.position))
    if model == Destination:
        position_query = position_query.filter_by(user_id=user_id)
    elif model == Activity:
        position_query = position_query.filter_by(destination_id=destination_id)

    # Set position
    highest_position = position_query.scalar()
    new_position = (highest_position + 1) if highest_position is not None else 1
    data['position'] = new_position

    # Set ID of required relationship
    if user_id:
        data['user_id'] = user_id
    if destination_id:
        data['destination_id'] = destination_id

    # Init new entry
    new_entry = model(**data)

    # Safe new entry in db
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': f'{model.__name__} added successfully!', model.__name__.lower(): model_to_dict(new_entry)}), 201

# Get entry by ID
def get_entry(model, entry_id, user_id):

    # Get entry and return error if one is thrown
    entry = check_existence_and_permission(model, entry_id, user_id)
    if isinstance(entry, tuple):
        return entry

    return model_to_dict(entry), 200

# Edit entry in db
def edit_entry(model, entry_id, data, allowed_fields=None, user_id=None):

    # Set allowed fields to standard value
    if allowed_fields is None:
        allowed_fields = [key for key in data.keys() if not key.startswith('_')]

    # Get entry
    entry = model.query.filter_by(id=entry_id).first()
    if not entry:
        return jsonify({'error': f'{model} not found'}), 404

    # Edit allowed fields only
    for key, value in data.items():
        if key in allowed_fields:
            setattr(entry, key, value)

    # Commit changings in db
    db.session.commit()

    return jsonify({'message': f'Updated {model.__name__} successfully!', model.__name__.lower(): model_to_dict(entry)}), 200

# Reorder items
def reorder_items(model, filter_by, new_order, item_name):

    # Check if there is new order from data
    if not new_order:
        return jsonify({'error': f'The list of {item_name} is missing'}), 400

    # Get all items needed as dict
    items = model.query.filter_by(**filter_by).all()
    item_dict = {item.id: item for item in items}

    # Check if all the IDs exist
    if set(map(int, new_order)) != set(item_dict.keys()):
        return jsonify({'error': f'Invalid or missing IDs of {item_name}'}), 400

    # Reorder items
    for new_position, item_id in enumerate(new_order, start=1):
        item = item_dict[int(item_id)]
        item.position = new_position

    # Update db
    db.session.commit()

    return jsonify({'message': f'Reordered {item_name.capitalize()} successfully!'}), 200

# Delete item
def delete_item(model, item_id):

    # Get item by id
    item = model.query.filter_by(id=item_id).first()

    # Delete item in db
    db.session.delete(item)
    db.session.commit()

    # Logout if item is user
    if model == User:
        logout_user()

    return jsonify({'message': f'{model.__name__} deleted successfully!'}), 200

