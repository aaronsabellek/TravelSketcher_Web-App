# HILFSVARIABLEN UND -FUNKTIONEN FÜR DIE TESTS

url = "http://127.0.0.1:5000"

registration_data = {
        "username": "testuser_123",
        "email": "testuser@example.com",
        "password": "testpassword123!",
        "city": "Leipzig",
        "longitude": "12.3731",
        "latitude": "51.3397",
        "country": "Deutschland",
        "currency": "EUR"
}

updated_profile_data = {
        "username": "testuser",
        "email": "testuser@example_edited.com",
        "city": "Leipzig",
        "longitude": "12.3731",
        "latitude": "51.3397",
        "country": "Deutschland",
        "currency": "EUR"
}

original_profile_data = {
    "username": "testuser",
        "email": "testuser@example.com",
        "city": "Leipzig",
        "longitude": "12.3731",
        "latitude": "51.3397",
        "country": "Deutschland",
        "currency": "EUR"
}

login_data_username = {
    'identifier': 'testuser',
    'password': 'testpassword123!'
}

login_data_email = {
    'identifier': 'testuser@example.com',
    'password': 'testpassword123!'
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

updated_destination_data = {
    'title': 'Turku',
    'country': 'Finland',
    'img_link': 'https://example.com/turku.jpg',
    'duration': '5 days',
    'tags': 'city, culture, nature',
    'status': 'planned',
    'time': 'summer',
    'accomodation_link': 'https://example.com/turku-hotel',
    'pricing': '1200',
    'trip_pricing_flight': '300',
    'trip_pricing_no_flight': '900',
    'travel_duration_flight': '2h',
    'travel_duration_no_flight': '20h',
    'longitude': '24.941',
    'latitude': '60.173',
    'description': 'Experience the Nordic charm of Turku with its unique mix of modern architecture and historical sites.',
    'free_text': 'Don’t miss the Turku castle and the traditional Finnish saunas!'
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

updated_activity_data = {
    'title': 'Turku Sightseeing Tour',
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
    'description': 'Explore Turku’s iconic landmarks.',
    'free_text': 'Includes a professional guide and transport between locations.',
    'destination_id': 1
}