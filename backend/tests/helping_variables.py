import uuid

# Standard URL
url = 'http://127.0.0.1:5000'

# Mailhog URLs
mailhog_v2 = 'http://localhost:8025/api/v2/messages'
mailhog_v1 = 'http://localhost:8025/api/v1/messages'

# Dummy data for conftest
dummy_data = {
    'user': {
        'id': str(uuid.uuid4()),
        'username': 'test_user',
        'email': 'test_user@example.com',
        'password': 'testpassword123!',
        'city': 'Leipzig',
        'longitude': '12.3731',
        'latitude': '51.3397',
        'country': 'Germany',
        'currency': 'EUR',
        'is_email_verified': True
    },
    'second_user': {
        'id': str(uuid.uuid4()),
        'username': 'second_user',
        'email': 'second_user@example.com',
        'password': 'testpassword123!',
        'city': 'Dresden',
        'longitude': '13.7372',
        'latitude': '51.0504',
        'country': 'Germany',
        'currency': 'EUR',
        'is_email_verified': True
    },
    'destinations': [
        {
            'id': str(uuid.uuid4()),
            'title': 'Paris',
            'country': 'France',
            'position': 1,
            'activities': [
                {'id': str(uuid.uuid4()),'title': 'Visit the Eiffel Tower', 'country': 'France', 'position': 1},
                {'id': str(uuid.uuid4()),'title': 'Explore the Louvre Museum', 'country': 'France', 'position': 2},
                {'id': str(uuid.uuid4()),'title': 'Visit Notre-Dame Cathedral', 'country': 'France', 'position': 3},
                {'id': str(uuid.uuid4()),'title': 'Take a boat trip on the Seine', 'country': 'France', 'position': 4},
                {'id': str(uuid.uuid4()),'title': 'Stroll along the Champs-Élysées', 'country': 'France', 'position': 5}
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'New York',
            'country': 'USA',
            'position': 2,
            'activities': [
                {'id': str(uuid.uuid4()),'title': 'Walk through Central Park', 'country': 'USA', 'position': 1},
                {'id': str(uuid.uuid4()),'title': 'Visit the Statue of Liberty', 'country': 'USA', 'position': 2}
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Tokyo',
            'country': 'Japan',
            'position': 3,
            'activities': []
        }
    ],
    'second_destinations': [
        {
            'id': str(uuid.uuid4()),
            'title': 'London',
            'country': 'United Kingdom',
            'position': 1,
            'activities': [
                {'id': str(uuid.uuid4()),'title': 'See Big Ben', 'country': 'United Kingdom', 'position': 1},
                {'id': str(uuid.uuid4()),'title': 'Ride the London Eye', 'country': 'United Kingdom', 'position': 2},
                {'id': str(uuid.uuid4()),'title': 'Explore the Tower of London', 'country': 'United Kingdom', 'position': 3},
                {'id': str(uuid.uuid4()),'title': 'Visit Camden Market', 'country': 'United Kingdom', 'position': 4},
                {'id': str(uuid.uuid4()),'title': 'Boat tour on the Thames', 'country': 'United Kingdom', 'position': 5}
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'id': str(uuid.uuid4()),
            'title': 'Sydney',
            'country': 'Australia',
            'position': 2,
            'activities': [
                {'id': str(uuid.uuid4()),'title': 'Visit the Sydney Opera House', 'country': 'Australia', 'position': 1},
                {'id': str(uuid.uuid4()),'title': 'Relax at Bondi Beach', 'country': 'Australia', 'position': 2},
                {'id': str(uuid.uuid4()),'title': 'Cross the Harbour Bridge', 'country': 'Australia', 'position': 3}
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Rio de Janeiro',
            'country': 'Brazil',
            'position': 3,
            'activities': [
                {'id': str(uuid.uuid4()),'title': 'See Christ the Redeemer', 'country': 'Brazil', 'position': 1},
                {'id': str(uuid.uuid4()),'title': 'Relax at Copacabana Beach', 'country': 'Brazil', 'position': 2},
                {'id': str(uuid.uuid4()),'title': 'Climb Sugarloaf Mountain', 'country': 'Brazil', 'position': 3}
            ]
        }
    ]
}

# Variables for dummy user
user = dummy_data['user']
second_user = dummy_data['second_user']

username = user['username']
email = user['email']
password = user['password']
city = user['city']
longitude = user['longitude']
latitude = user['latitude']
country = user['country']
currency = user['currency']
is_email_verified = user['is_email_verified']

# User IDs
user_main_id = user['id']
user_second_id = second_user['id']

# Destination IDs of main user
destinations = dummy_data['destinations']
dest_main_id = destinations[0]['id']
dest_2_id = destinations[1]['id']
dest_3_id = destinations[2]['id']

# First destination ID of second user
dest_second_user_id = dummy_data['second_destinations'][0]['id']

# Activities of first destination of main user
activities = dummy_data['destinations'][0]['activities']
act_main_id = activities[0]['id']
act_2_id = activities[1]['id']
act_3_id = activities[2]['id']
act_4_id = activities[3]['id']
act_5_id = activities[4]['id']

# First activity of second user
act_second_user_id = dummy_data['second_destinations'][0]['activities'][0]['id']

# Wrong id
wrong_id = '11111111-1111-1111-1111-111111111111'

# Variables for registration
registration_base_data = {
        **user,
        'username': 'test_user_registration',
        'email': 'registration@example.com',
}

# Variable for dummy second_user
second_user = dummy_data['second_user']

# Variable for first destination
destination = dummy_data['destinations'][0]

# Login data with username
login_data_username = {
    'identifier': user['username'],
    'password': user['password']
}

# Data for new destianation
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

# Data for new activity
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

# Data to login with username
login_data_username = {
    'identifier': user['username'],
    'password': user['password']
}

