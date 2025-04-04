import uuid

from tests.helpers.variables import (
    dest_main_id,
    dest_2_id,
    dest_3_id,
    dest_second_user_id,
    wrong_id
)

# Base data for new destianation
new_destination = {
    'id': str(uuid.uuid4()),
    'title': 'Helsinki',
    'country': 'Finland',
    'img_link': 'https://example.com/helsinki.jpg',
    'duration': '5 days',
    'tags': 'city, culture, nature',
    'status': 'planned',
    'time': 'summer',
    'accomodation_link': 'https://example.com/helsinki-hotel',
    'pricing': '1200',
    'trip_pricing_flight': '300',
    'trip_pricing_no_flight': '900',
    'travel_duration_flight': '2h',
    'travel_duration_no_flight': '20h',
    'longitude': '24.941',
    'latitude': '60.173',
    'description': 'Experience the Nordic charm of Helsinki with its unique mix of modern architecture and historical sites.',
    'free_text': 'Don’t miss the Suomenlinna sea fortress and the traditional Finnish saunas!'
}

# Test data for adding destination to database
add_destination = [
    # Wrong id
    {**new_destination, 'id': dest_main_id, 'expected_status': 500, 'expected_message': 'A database error occurred'},
    # Required field empty
    {**new_destination, 'title': '', 'expected_status': 400, 'expected_message': 'Title is required'},

    # Successfull test case
    {**new_destination, 'expected_status': 201, 'expected_message': 'Destination added successfully!'},
    # Successfull test case with unrequired field empty
    {**new_destination, 'country': '', 'expected_status': 201, 'expected_message': 'Destination added successfully!'}
]

# Test data to get specific destination of user
get_destination = [
    # Destination belongs to another user
    {'id': dest_second_user_id, 'expected_status': 403, 'expected_message': 'Destination not permitted'},
    # Destination does not exist
    {'id': wrong_id, 'expected_status': 404, 'expected_message': 'Destination not found'},

    # Successfull test case
    {'id': dest_main_id, 'expected_status': 200}
]

# Test data to edit destination
edit_destination = [
    # Destination belongs to another user
    {**new_destination, 'id': dest_second_user_id, 'expected_status': 403, 'expected_message': 'Destination not permitted'},
    # Destination does not exist
    {**new_destination, 'id': wrong_id, 'expected_status': 404, 'expected_message': 'Destination not found'},
    # Required field is empty
    {'title': '', 'id': dest_main_id, 'expected_status': 400, 'expected_message': 'Title is required'},

    # Successfull test case
    {**new_destination, 'id': dest_main_id, 'expected_status': 200, 'expected_message': 'Updated Destination successfully!'}
]

# Test data to reorder destinations
reorder_destinations = [
    # New order missing
    {'new_order': [], 'expected_status': 400, 'expected_message': 'The new order of destinations is missing'},
    # Destination belongs to different user
    {'new_order': [dest_main_id, dest_second_user_id, dest_2_id], 'expected_status': 400, 'expected_message': 'Invalid or missing IDs for destinations'},
    # Destination does not exist
    {'new_order': [dest_main_id, wrong_id, dest_2_id], 'expected_status': 400, 'expected_message': 'Invalid or missing IDs for destinations'},
    # Dublicates in new order
    {'new_order': [dest_main_id, dest_3_id, dest_3_id], 'expected_status': 400, 'expected_message': 'Invalid or missing IDs for destinations'},
    # New order is too short
    {'new_order': [dest_main_id, dest_3_id], 'expected_status': 400, 'expected_message': 'Invalid or missing IDs for destinations'},

    # Successfull test case
    {'new_order': [dest_main_id, dest_3_id, dest_2_id], 'expected_status': 200, 'expected_message': 'Reordered Destinations successfully!'},
]

# Test data to delete destination
delete_destination = [
    # Destination does not belong to user
    {'destination_id': dest_second_user_id, 'expected_status': 403, 'expected_message': 'Destination not permitted'},
    # Destination does not exist
    {'destination_id': wrong_id, 'expected_status': 404, 'expected_message': 'Destination not found'},

    # Successfull test case
    {'destination_id': dest_main_id, 'expected_status': 200, 'expected_message': 'Destination deleted successfully!'}
]

