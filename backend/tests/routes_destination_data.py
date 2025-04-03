from tests.helping_variables import new_destination


# Test add destination
add_destination = [
    # Wrong id
    {**new_destination, 'id': 2, 'expected_status': 500, 'expected_message': 'A database error occurred'},
    # Required field empty
    {**new_destination, 'title': '', 'expected_status': 400, 'expected_message': 'Title is required'},

    # Successfull test case
    {**new_destination, 'expected_status': 201, 'expected_message': 'Destination added successfully!'},
    # Successfull test case with unrequired field empty
    {**new_destination, 'country': '', 'expected_status': 201, 'expected_message': 'Destination added successfully!'}
]

# Test get destination
get_destination = [
    # Destination belongs to another user
    {'destination_id': 4, 'expected_status': 403, 'expected_message': 'Destination not permitted'},
    # Destination does not exist
    {'destination_id': 10, 'expected_status': 404, 'expected_message': 'Destination not found'},

    # Successfull test case
    {'destination_id': 1, 'expected_status': 200}
]

# Test edit destination
edit_destination = [
    # Destination belongs to another user
    {**new_destination, 'destination_id': 4, 'expected_status': 403, 'expected_message': 'Destination not permitted'},
    # Destination does not exist
    {**new_destination, 'destination_id': 10, 'expected_status': 404, 'expected_message': 'Destination not found'},
    # Required field is empty
    {'title': '', 'destination_id': 1, 'expected_status': 400, 'expected_message': 'Title is required'},

    # Successfull test case
    {**new_destination, 'destination_id': 1, 'expected_status': 200, 'expected_message': 'Updated Destination successfully!'}
]

# Test reorder destinations
reorder_destinations = [
    # New order missing
    {'new_order': [], 'expected_status': 400, 'expected_message': 'The new order of destinations is missing'},
    # ID is from different user
    {'new_order': [1, 4, 2], 'expected_status': 400, 'expected_message': 'Invalid or missing IDs of destinations'},
    # ID does not exist
    {'new_order': [1, 10, 2], 'expected_status': 400, 'expected_message': 'Invalid or missing IDs of destinations'},
    # New order is too long
    {'new_order': [1, 3, 2, 3], 'expected_status': 400, 'expected_message': 'Length of new order does not match length of destinations'},
    # New order is too short
    {'new_order': [1, 3], 'expected_status': 400, 'expected_message': 'Length of new order does not match length of destinations'},

    # Successfull test case
    {'new_order': [1, 3, 2], 'expected_status': 200, 'expected_message': 'Reordered Destinations successfully!'},
]

# Test delete destination
delete_destination = [
    # Destination does not belong to user
    {'destination_id': 4, 'expected_status': 403, 'expected_message': 'Destination not permitted'},
    # Destination does not exist
    {'destination_id': 10, 'expected_status': 404, 'expected_message': 'Destination not found'},

    # Successfull test case
    {'destination_id': 1, 'expected_status': 200, 'expected_message': 'Destination deleted successfully!'}
]

