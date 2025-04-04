

# Test data to search in entries
search_data = [
    # Empty search query
    {'query': '', 'type': 'both', 'expected_status': 400, 'expected_message': 'Search query required'},

    # Search non existent word
    {'query': 'Arctica', 'type': 'both', 'expected_results': 0, 'expected_status': 200},
    # Search word from different user
    {'query': 'Kingdom', 'type': 'both', 'expected_results': 0, 'expected_status': 200},
    # Search position (ignored)
    {'query': 1, 'type': 'both', 'expected_results': 0, 'expected_status': 200},

    # Search in destinations
    {'query': 'France', 'type': 'destination', 'expected_results': 1, 'expected_status': 200},
    # Search in activities
    {'query': 'France', 'type': 'activity', 'expected_results': 5, 'expected_status': 200},
    # Search in both
    {'query': 'France', 'type': 'both', 'expected_results': 6, 'expected_status': 200},
    # Search with unknown resource type
    {'query': 'France', 'type': 'unknown_type', 'expected_results': 6, 'expected_status': 200},
    # Search only part of word
    {'query': 'Fra', 'type': 'both', 'expected_results': 6, 'expected_status': 200},
    # Search with big characters only
    {'query': 'FRANCE', 'type': 'both', 'expected_results': 6, 'expected_status': 200}
]

