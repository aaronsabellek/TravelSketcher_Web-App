import uuid

# Dummy data for tests
dummy_data = {
    'user': {
        'id': str(uuid.uuid4()),
        'username': 'test_user',
        'email': 'test_user@example.com',
        'password': 'Testpassword123!',
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
        'password': 'Testpassword123!',
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

