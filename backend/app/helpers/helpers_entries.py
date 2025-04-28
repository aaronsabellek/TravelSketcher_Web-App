from flask import jsonify, request
from flask_login import logout_user, current_user

from app import db
from app.models import User, Destination, Activity
from app.helpers.helpers import model_to_dict, models_to_list


def check_existence_and_permission(model, entry_id):
    """Checks existence and user permission of entry"""

    # Check if entry exists
    entry = model.query.filter_by(id=entry_id).first()
    if not entry:
            return {'error': f'{model.__name__} not found'}, 404

    # Check permission of user
    if model == Destination:
        owner_id = entry.owner.id
    elif model == Activity:
        owner_id = entry.destination.owner.id

    if owner_id != current_user.id:
        return {'error': f'{model.__name__} not permitted'}, 403

    return entry


def create_entry(model, data, user_id=None, destination_id=None):
    """Creates entry in database"""

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


def get_paginated_entries(model, filters=None, order_by=None, model_key=None, extra_data=None):
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=12, type=int)

    query = model.query
    if filters:
        query = query.filter_by(**filters)

    if order_by:
        query = query.order_by(order_by)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items

    response_data = {
        model_key or model.__tablename__: models_to_list(items),
        'has_more': pagination.has_next,
    }

    if extra_data:
        response_data.update(extra_data)

    return jsonify(response_data), 200


def edit_entry(model, entry_id, data, allowed_fields=None):
    """Edits entry in database"""

    # Set allowed fields to standard value
    if allowed_fields is None:
        allowed_fields = [key for key in data.keys() if not key.startswith('_')]

    # If not user: Check for required title
    if model != User:
        if not data.get('title') or data['title'] == '':
            return jsonify({'error': 'Title is required'}), 400

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


def update_entry_field(model, entry_id, field_name, new_value):
    """Updates a single field of an entry"""

    # Check if instance exists in database
    instance = model.query.filter_by(id=entry_id).first()
    if not instance:
        return jsonify({'error': f'{model.__name__} with ID {entry_id} not found'}), 404

    # Check if field exists in model
    if not hasattr(instance, field_name):
        return jsonify({'error': f'Field {field_name} not found in {model.__name__}'}), 400

    # Updpate data
    setattr(instance, field_name, new_value)

    # Commit changes in database
    db.session.commit()

    return jsonify({'message': f'Updated {model.__name__} successfully!'}), 200


def reorder_entries(model, filter_by, new_order, entry_name):
    """Reorders entries in database based on IDs"""

    # Check if new order exists
    if not new_order:
        return jsonify({'error': f'The new order of {entry_name} is missing'}), 400

     # Get all current entries for the user
    entries = model.query.filter_by(**filter_by).all()
    entries_dict = {str(entry.id): entry for entry in entries}

     # Check for invalid or missing IDs
    if set(new_order) != set(entries_dict.keys()):
        return jsonify({
            'error': f'Invalid or missing IDs for {entry_name}',
            'expected': list(entries_dict.keys()),
            'got': new_order
        }), 400

    # Reorder positions
    for new_position, item_id in enumerate(new_order, start=1):
        item = entries_dict[item_id]
        item.position = new_position

    db.session.commit() # Commit changes in database

    return jsonify({
        'message': f'Reordered {entry_name.capitalize()} successfully!',
        'new_order': [str(item.id) for item in sorted(entries_dict.values(), key=lambda x: x.position)]
    }), 200


def delete_entry(model, entry_id):
    """Deletes entry from database"""

    # Get item by id
    entry = model.query.filter_by(id=entry_id).first()

    # Delete item in db
    db.session.delete(entry)
    db.session.commit()

    # Logout if item is user
    if model == User:
        logout_user()

    return jsonify({'message': f'{model.__name__} deleted successfully!'}), 200

