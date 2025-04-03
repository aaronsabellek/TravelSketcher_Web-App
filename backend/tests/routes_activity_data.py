from tests.helping_variables import new_activity

# Test data to add activity to database
add_activity = [
    # Wrong id
    {**new_activity, 'id': 2, 'expected_status': 500, 'expected_message': 'A database error occurred'},
    # Destination does not belong to user
    {**new_activity, 'destination_id': 4, 'expected_status': 403, 'expected_message': 'Destination not permitted'},
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
    {'destination_id': 4, 'expected_status': 403, 'expected_message': 'Destination not permitted'},
    # Destination does not exist
    {'destination_id': 10, 'expected_status': 404, 'expected_message': 'Destination not found'},

    # Successfull test case
    {'destination_id': 1, 'expected_status': 200},
    # Successfull test case but with no activities
    {'destination_id': 3, 'expected_status': 200, 'expected_message': "Destination 'Tokyo' has no activities yet"}
]

# Test data to get specific activity
get_activity = [
    # Activity belongs to another user
    {'activity_id': 10, 'expected_status': 403, 'expected_message': 'Activity not permitted'},
    # Activity does not exist
    {'activity_id': 30, 'expected_status': 404, 'expected_message': 'Activity not found'},

    # Successfull test case
    {'activity_id': 1, 'expected_status': 200}
]

# Test data to edit activity
edit_activity = [
    # Activtiy belongs to another user
    {**new_activity, 'activity_id': 10, 'expected_status': 403, 'expected_message': 'Activity not permitted'},
    # Activity does not exist
    {**new_activity, 'activity_id': 30, 'expected_status': 404, 'expected_message': 'Activity not found'},
    # Required field is empty
    {'title': '', 'activity_id': 1, 'expected_status': 400, 'expected_message': 'Title is required'},

    # Successfull test case
    {**new_activity, 'activity_id': 1, 'expected_status': 200, 'expected_message': 'Updated Activity successfully!'}
]

# Test data to reorder activities of specific destination
reorder_activities = [
    # Destination belongs to another user
    {'destination_id': 4, 'new_order': [1, 3, 2, 4, 5], 'expected_status': 403, 'expected_message': 'Destination not permitted'},
    # Destination does not exist
    {'destination_id': 10, 'new_order': [1, 3, 2, 4, 5], 'expected_status': 404, 'expected_message': 'Destination not found'},
    # New order missing
    {'destination_id': 1, 'new_order': [], 'expected_status': 400, 'expected_message': 'The new order of activities is missing'},
    # New order is too long
    {'destination_id': 1, 'new_order': [1, 3, 2, 4, 5, 6], 'expected_status': 400, 'expected_message': 'Length of new order does not match length of activities'},
    # New order is too short
    {'destination_id': 1, 'new_order': [1, 3, 2, 4], 'expected_status': 400, 'expected_message': 'Length of new order does not match length of activities'},

    # Successfull test case
    {'destination_id': 1, 'new_order': [1, 3, 2, 4, 5], 'expected_status': 200, 'expected_message': 'Reordered Activities successfully!'}
]

# Test data to delete specific activity from database
delete_activity = [
    # Destination does not belong to user
    {'activity_id': 10, 'expected_status': 403, 'expected_message': 'Activity not permitted'},
    # Destination does not exist
    {'activity_id': 30, 'expected_status': 404, 'expected_message': 'Activity not found'},

    # Successfull test case
    {'activity_id': 1, 'expected_status': 200, 'expected_message': 'Activity deleted successfully!'}
]

