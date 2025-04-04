import uuid

from tests.helpers.variables import (
    dest_main_id,
    dest_3_id,
    dest_second_user_id,
    act_main_id,
    act_2_id,
    act_3_id,
    act_4_id,
    act_5_id,
    act_second_user_id,
    wrong_id
)

# Base data for new activity
new_activity = {
    'id': str(uuid.uuid4()),
    'title': 'Suomenlina Fortress',
    'country': 'Finland',
    'duration': '3-6h',
    'pricing': 'Free',
    'status': 'Planned',
    'web_link': 'https://suomenlina.fi',
    'img_link': 'https://suomenlina.fi/img',
    'tags': 'Fortress,Military,Island',
    'trip_duration': '0,5h',
    'trip_pricing': '5 EUR',
    'longitude': '24.59',
    'latitude': '60.852',
    'description': 'Old fortress in the Baltic Sea',
    'free_text': 'Combine with boat tour through the Archipelago',
    'destination_id': dest_main_id
}

# Test data to add activity to database
add_activity = [
    # Wrong id
    {**new_activity, 'id': act_second_user_id, 'expected_status': 500, 'expected_message': 'A database error occurred'},
    # Destination does not belong to user
    {**new_activity, 'destination_id': dest_second_user_id, 'expected_status': 403, 'expected_message': 'Destination not permitted'},
    # Required field empty
    {**new_activity, 'title': '', 'expected_status': 400, 'expected_message': 'Title is required'},

    # Successfull test case
    {**new_activity, 'expected_status': 201, 'expected_message': 'Activity added successfully!'},
    # Successfull test case with unrequired field empty
    {**new_activity, 'country': '', 'expected_status': 201, 'expected_message': 'Activity added successfully!'}
]

# Test data to get all activities of specific destination
get_all = [
    # Destination belongs to another user
    {'destination_id': dest_second_user_id, 'expected_status': 403, 'expected_message': 'Destination not permitted'},
    # Destination does not exist
    {'destination_id': wrong_id, 'expected_status': 404, 'expected_message': 'Destination not found'},

    # Successfull test case
    {'destination_id': dest_main_id, 'expected_status': 200},
    # Successfull test case but with no activities
    {'destination_id': dest_3_id, 'expected_status': 200, 'expected_message': "Destination 'Tokyo' has no activities yet"}
]

# Test data to get specific activity
get_activity = [
    # Activity belongs to another user
    {'activity_id': act_second_user_id, 'expected_status': 403, 'expected_message': 'Activity not permitted'},
    # Activity does not exist
    {'activity_id': wrong_id, 'expected_status': 404, 'expected_message': 'Activity not found'},

    # Successfull test case
    {'activity_id': act_main_id, 'expected_status': 200}
]

# Test data to edit activity
edit_activity = [
    # Activtiy belongs to another user
    {**new_activity, 'id': act_second_user_id, 'expected_status': 403, 'expected_message': 'Activity not permitted'},
    # Activity does not exist
    {**new_activity, 'id': wrong_id, 'expected_status': 404, 'expected_message': 'Activity not found'},
    # Required field is empty
    {**new_activity, 'id': act_main_id, 'title': '', 'expected_status': 400, 'expected_message': 'Title is required'},

    # Successfull test case
    {**new_activity, 'id': act_main_id, 'expected_status': 200, 'expected_message': 'Updated Activity successfully!'}
]

# Test data to reorder activities of specific destination
new_order = [act_main_id, act_3_id, act_2_id, act_4_id, act_5_id]

reorder_activities = [
    # New order missing
    {'destination_id': dest_main_id, 'new_order': [], 'expected_status': 400, 'expected_message': 'The new order of activities is missing'},
    # Destination belongs to different user
    {'destination_id': dest_second_user_id, 'new_order': new_order, 'expected_status': 403, 'expected_message': 'Destination not permitted'},
    # Destination does not exist
    {'destination_id': wrong_id, 'new_order': new_order, 'expected_status': 404, 'expected_message': 'Destination not found'},
    # Dublicates in new order
    {'destination_id': dest_main_id, 'new_order': [act_main_id, act_3_id, act_2_id, act_4_id, act_4_id], 'expected_status': 400, 'expected_message': 'Invalid or missing IDs for activities'},
    # New order is too short
    {'destination_id': dest_main_id, 'new_order': [act_main_id, act_3_id, act_2_id, act_4_id], 'expected_status': 400, 'expected_message': 'Invalid or missing IDs for activities'},

    # Successfull test case
    {'destination_id': dest_main_id, 'new_order': new_order, 'expected_status': 200, 'expected_message': 'Reordered Activities successfully!'}
]

# Test data to delete specific activity from database
delete_activity = [
    # Activity does not belong to user
    {'activity_id': act_second_user_id, 'expected_status': 403, 'expected_message': 'Activity not permitted'},
    # Activity does not exist
    {'activity_id': wrong_id, 'expected_status': 404, 'expected_message': 'Activity not found'},

    # Successfull test case
    {'activity_id': act_main_id, 'expected_status': 200, 'expected_message': 'Activity deleted successfully!'}
]

