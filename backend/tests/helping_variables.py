import uuid


# HILFSVARIABLEN UND -FUNKTIONEN FÜR DIE TESTS

url = 'http://127.0.0.1:5000'

mailhog_v2 = 'http://localhost:8025/api/v2/messages'

mailhog_v1 = 'http://localhost:8025/api/v1/messages'

dummy_data = {
    'user': {
        'username': 'test_user',
        'email': 'test_user@example.com',
        'password': 'testpassword123!',
        'city': 'Leipzig',
        'longitude': '12.3731',
        'latitude': '51.3397',
        'country': 'Deutschland',
        'currency': 'EUR',
        'is_email_verified': True
    },
    'destinations': [
        {
            'title': 'Paris',
            'country': 'Frankreich',
            'position': 1,
            'activities': [
                {'title': 'Eiffelturm besuchen', 'country': 'Frankreich', 'position': 1},
                {'title': 'Louvre Museum', 'country': 'Frankreich', 'position': 2},
                {'title': 'Notre-Dame Cathedral besichtigen', 'country': 'Frankreich', 'position': 3},
                {'title': 'Bootsfahrt auf der Seine', 'country': 'Frankreich', 'position': 4},
                {'title': 'Champs-Élysées spazieren', 'country': 'Frankreich', 'position': 5}
            ]
        },
        {
            'title': 'New York',
            'country': 'USA',
            'position': 2,
            'activities': [
                {'title': 'Central Park', 'country': 'USA', 'position': 1},
                {'title': 'Statue of Liberty', 'country': 'USA', 'position': 2}
            ]
        },
        {
            'title': 'Tokyo',
            'country': 'Japan',
            'position': 3,
            'activities': [
                {'title': 'Shibuya Crossing', 'country': 'Japan', 'position': 1},
                {'title': 'Mount Fuji', 'country': 'Japan', 'position': 2}
            ]
        }
    ]
}

registration_base_data = {
        "username": f"test_user_registration",
        "email": f"registration@example.com",
        "password": "testpassword123!",
        "city": "Leipzig",
        "longitude": "12.3731",
        "latitude": "51.3397",
        "country": "Deutschland",
        "currency": "EUR"
}

registration_data = [
    # Empty required field
    {**registration_base_data, 'country': '', 'expected_status': 400, 'expected_message': 'Field(s) missing!'},
    # Wrong Email format
    {**registration_base_data, 'email': 'testemail', 'expected_status': 400, 'expected_message': 'Wrong Email format!'},
    # Short password
    {**registration_base_data, 'password': 's1!', 'expected_status': 400, 'expected_message': 'Passwort has to have at least 8 characters!'},
    # Password has no letter
    {**registration_base_data, 'password': '12345678!', 'expected_status': 400, 'expected_message': 'Passwort has to have at least one letter!'},
    # Password has no digit
    {**registration_base_data, 'password': 'testpassword!', 'expected_status': 400, 'expected_message': 'Passwort has to have at least one digit!'},
    # Password has no special character
    {**registration_base_data, 'password': 'testpassword123', 'expected_status': 400, 'expected_message': 'Passwort has to have at least one special character!'},
    # Existing username
    {**registration_base_data, 'username': dummy_data['user']['username'], 'expected_status': 400, 'expected_message': 'Username is already taken!'},
    # Existing email
    {**registration_base_data, 'email': dummy_data['user']['email'], 'expected_status': 400, 'expected_message': 'Email is already taken!'},

    # Successfull test case
    {**registration_base_data, 'expected_status': 201, 'expected_message': 'Registration was successfull! A confirmation link has been sent.'}
]

verification_data = [
    # Email does not exist in db
    {'email': 'wrong_email@test-com', 'is_email_verified': False, 'token': True, 'expected_status': 404, 'expected_message': 'User not found!'},
    # User is already verified
    {'email': dummy_data['user']['email'], 'is_email_verified': True, 'token': True, 'expected_status': 200, 'expected_message': 'E-Mail has already been confirmed!'},
    # Token is wrong
    {'email': dummy_data['user']['email'], 'is_email_verified': False, 'token': False, 'expected_status': 400, 'expected_message': 'Invalid or expired token!'},

    # Successfull test case
    {'email': dummy_data['user']['email'], 'is_email_verified': False, 'token': True, 'expected_status': 200, 'expected_message': 'E-Mail confirmed successfully!'}
]

updated_profile_data = {
        "username": f"{uuid.uuid4().hex}",
        "email": f"{uuid.uuid4().hex}@example.com",
        "password": dummy_data['user']['password'],
        "city": dummy_data['user']['city'],
        "longitude": dummy_data['user']['longitude'],
        "latitude": dummy_data['user']['latitude'],
        "country": dummy_data['user']['country'],
        "currency": dummy_data['user']['currency']
}

updated_password = {
    'new_password_1': 'new_password123!',
    'new_password_2': 'new_password123!'
}

login_data_username = {
    'identifier': dummy_data['user']['username'],
    'password': dummy_data['user']['password']
}

login_data_email = {
    'identifier': dummy_data['user']['email'],
    'password': dummy_data['user']['password']
}

destination_data = {
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

activity_data = {
    'title': 'Helsinki Sightseeing Tour',
    'country': 'Finland',
    'duration': '3 hours',
    'pricing': '50',
    'status': 'available',
    'web_link': 'https://example.com/helsinki-tour',
    'img_link': 'https://example.com/helsinki-tour.jpg',
    'tags': 'sightseeing, history, culture',
    'trip_duration': '1 day',
    'trip_pricing': '75',
    'longitude': '24.945',
    'latitude': '60.169',
    'description': 'Explore Helsinki’s iconic landmarks, including Senate Square, Temppeliaukio Church, and Market Square.',
    'free_text': 'Includes a professional guide and transport between locations.',
    'destination_id': 1
}

