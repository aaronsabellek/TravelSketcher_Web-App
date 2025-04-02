from tests.helping_variables import new_activity


# Test add activity
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

# Test get all activities of specific destination
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

# Test get specific activity
get_activity = [
    # Activity belongs to another user
    {'activity_id': 10, 'expected_status': 403, 'expected_message': 'Activity not permitted'},
    # Activity does not exist
    {'activity_id': 30, 'expected_status': 404, 'expected_message': 'Activity not found'},

    # Successfull test case
    {'activity_id': 1, 'expected_status': 200}
]