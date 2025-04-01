from tests.helping_variables import (
    dummy_data,
    email,
    city,
    longitude,
    latitude,
    country,
    currency,
    new_destination
)


# Test add destination
add_destination = [
    # Wrong id
    {**new_destination, 'id': 2, 'expected_status': 500, 'expected_message': 'A database error occurred'},
    # Required field empty
    {**new_destination, 'title': '', 'expected_status': 400, 'expected_message': 'Title is required'},

    # Successfull test case
    {**new_destination, 'expected_status': 201, 'expected_message': 'Destination added successfully!'},
    # Successfull test casse with unrequired field empty
    {**new_destination, 'country': '', 'expected_status': 201, 'expected_message': 'Destination added successfully!'}
]

# Test get specific destination
get_destination = [
    # Destination belongs to another user
    {'destination_id': 4, 'expected_status': 400, 'expected_message': 'Destination not permitted'},
    # Destination does not exist
    {'destination_id': 10, 'expected_status': 404, 'expected_message': 'Destination not found'},

    # Successfull test casse with unrequired field empty
    {'destination_id': 1, 'expected_status': 200}
]

