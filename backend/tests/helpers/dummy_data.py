import uuid

# Dummy data for tests
dummy_data = {
    'user': {
        'id': str(uuid.uuid4()),
        'username': 'test_user',
        'email': 'test_user@example.com',
        'password': 'Testpassword123!',
        'city': 'Leipzig',
        'country': 'Germany',
        'is_email_verified': True
    },
    'second_user': {
        'id': str(uuid.uuid4()),
        'username': 'second_user',
        'email': 'second_user@example.com',
        'password': 'Testpassword123!',
        'city': 'Dresden',
        'country': 'Germany',
        'is_email_verified': True
    },
    'destinations': [
        {
            'id': str(uuid.uuid4()),
            'title': 'Paris',
            'country': 'France',
            'position': 1,
            'tags': 'Eiffel Tower,Art & Museums,Romance,2h Flight',
            'img_link': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=1173&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'free_text': '',
            'activities': [
                {'id': str(uuid.uuid4()),'title': 'Visit the Eiffel Tower', 'country': 'France', 'web_link': 'https://www.toureiffel.paris/de', 'img_link': 'https://images.unsplash.com/photo-1492136344046-866c85e0bf04?q=80&w=1164&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 'position': 1},
                {'id': str(uuid.uuid4()),'title': 'Explore the Louvre Museum', 'country': 'France', 'web_link': 'https://www.louvre.fr/en', 'img_link': 'https://images.unsplash.com/photo-1567942585146-33d62b775db0?q=80&w=1009&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 'position': 2},
                {'id': str(uuid.uuid4()),'title': 'Visit Notre-Dame Cathedral', 'country': 'France', 'web_link': 'https://www.notredamedeparis.fr/', 'img_link': 'https://images.unsplash.com/photo-1574870310056-79c4b3c7d449?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 'position': 3},
                {'id': str(uuid.uuid4()),'title': 'Take a boat trip on the Seine', 'country': 'France', 'web_link': '', 'img_link': '', 'position': 4},
                {'id': str(uuid.uuid4()),'title': 'Stroll along the Champs-Élysées', 'country': 'France', 'web_link': '', 'img_link': '', 'position': 5}
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'New York',
            'country': 'USA',
            'position': 2,
            'tags': 'Skyline,Broadway,Central Park,9h flight',
            'img_link': 'https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'free_text': 'This is a note for New York.',
            'activities': [
                {'id': str(uuid.uuid4()),'title': 'Walk through Central Park', 'country': 'USA', 'web_link': '', 'img_link': 'https://images.unsplash.com/photo-1568515387631-8b650bbcdb90?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 'position': 1},
                {'id': str(uuid.uuid4()),'title': 'Visit the Statue of Liberty', 'country': 'USA', 'web_link': '', 'img_link': 'https://images.unsplash.com/photo-1485738422979-f5c462d49f74?q=80&w=1199&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 'position': 2}
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Tokyo',
            'country': 'Japan',
            'position': 3,
            'tags': 'Anime & Manga,Sushi,Mount Fuji,Temples & Shrines,15h flight',
            'img_link': 'https://plus.unsplash.com/premium_photo-1661914240950-b0124f20a5c1?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'free_text': 'This is a note for Tokyo.',
            'activities': []
        }
    ],
    'second_destinations': [
        {
            'id': str(uuid.uuid4()),
            'title': 'London',
            'country': 'United Kingdom',
            'img_link': '',
            'tags': 'Kingdom,Big Ben,2h Flight',
            'position': 1,
            'free_text': '',
            'activities': [
                {'id': str(uuid.uuid4()),'title': 'See Big Ben', 'country': 'United Kingdom', 'web_link': '', 'img_link': '','position': 1},
                {'id': str(uuid.uuid4()),'title': 'Ride the London Eye', 'country': 'United Kingdom', 'web_link': '', 'img_link': '','position': 2},
                {'id': str(uuid.uuid4()),'title': 'Explore the Tower of London', 'country': 'United Kingdom', 'web_link': '', 'img_link': '','position': 3},
                {'id': str(uuid.uuid4()),'title': 'Visit Camden Market', 'country': 'United Kingdom', 'web_link': '', 'img_link': '','position': 4},
                {'id': str(uuid.uuid4()),'title': 'Boat tour on the Thames', 'country': 'United Kingdom', 'web_link': '', 'img_link': '','position': 5}
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Sydney',
            'country': 'Australia',
            'tags': 'Kiwis,Pelicans,Pacific Ocean',
            'img_link': '',
            'position': 2,
            'free_text': '',
            'activities': [
                {'id': str(uuid.uuid4()),'title': 'Visit the Sydney Opera House', 'country': 'Australia', 'web_link': '', 'img_link': '','position': 1},
                {'id': str(uuid.uuid4()),'title': 'Relax at Bondi Beach', 'country': 'Australia', 'web_link': '', 'img_link': '','position': 2},
                {'id': str(uuid.uuid4()),'title': 'Cross the Harbour Bridge', 'country': 'Australia', 'web_link': '', 'img_link': '','position': 3}
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Rio de Janeiro',
            'country': 'Brazil',
            'tags': 'Carnival,South America',
            'img_link': '',
            'position': 3,
            'free_text': '',
            'activities': [
                {'id': str(uuid.uuid4()),'title': 'See Christ the Redeemer', 'country': 'Brazil', 'web_link': '', 'img_link': '','position': 1},
                {'id': str(uuid.uuid4()),'title': 'Relax at Copacabana Beach', 'country': 'Brazil', 'web_link': '', 'img_link': '','position': 2},
                {'id': str(uuid.uuid4()),'title': 'Climb Sugarloaf Mountain', 'country': 'Brazil', 'web_link': '', 'img_link': '','position': 3}
            ]
        }
    ]
}

