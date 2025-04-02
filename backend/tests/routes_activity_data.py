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

