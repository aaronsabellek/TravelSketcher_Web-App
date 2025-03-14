# HILFSVARIABLEN UND -FUNKTIONEN FÜR DIE TESTS

url = "http://127.0.0.1:5000"

registration_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123!"
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
        'title': 'Bali',
        'country': 'Indonesia',
        'img_link': 'https://example.com/bali.jpg',
        'duration': '2 weeks',
        'tags': 'beach, adventure, culture',
        'status': 'planned',
        'months': 'May, June, July',
        'accomodation_link': 'https://example.com/bali-hotel',
        'accomodation_price': '800',
        'accomodation_text': 'Luxury resort near the beach',
        'trip_duration': '14 days',
        'trip_price': '1500',
        'trip_text': 'Includes flights and tours',
        'free_text': 'Must try the local cuisine and visit hidden waterfalls!'
}

updated_destination_data = {
        'title': 'Updated Destination Title',
        'country': 'Italien',
        'img_link': 'https://example.com/new_image.jpg',
        'duration': '7 Tage',
        'tags': 'Strand, Sommer, Erholung',
        'status': 'aktiv',
        'months': 'Juni, Juli, August',
        'accomodation_link': 'https://example.com/accomodation',
        'accomodation_price': '1500',
        'accomodation_text': 'Luxushotel am Meer',
        'trip_duration': '10 Tage',
        'trip_price': '2500',
        'trip_text': 'Erholung pur an der Amalfiküste',
        'free_text': 'Jetzt buchen und sparen!'
}

activity_data = {
        'title': 'Wanderung im Gebirge',
        'country': 'Deutschland',
        'duration': '5 Stunden',
        'price': '20',
        'activity_text': 'Eine wunderschöne Wanderung mit atemberaubender Aussicht.',
        'status': 'aktiv',
        'web_link': 'http://example.com',
        'img_link': 'http://example.com/image.jpg',
        'tags': 'Wandern, Berge, Natur',
        'trip_duration': '7 Tage',
        'trip_price': '500',
        'trip_text': 'Entdecke die Berge in 7 Tagen',
        'free_text': 'Die Wanderung kann individuell angepasst werden.',
        'destination_id': 1
}

updated_activity_data = {
        'title': 'Neue Aktivität',
        'country': 'Deutschland',
        'duration': '5',
        'price': '150.0',
        'activity_text': 'Dies ist die Beschreibung der neuen Aktivität.',
        'status': 'Aktiv',
        'web_link': 'https://example.com',
        'img_link': 'https://example.com/image.jpg',
        'tags': 'Abenteuer Natur',
        'trip_duration': '7',
        'trip_price': '500.0',
        'trip_text': 'Detaillierte Beschreibung der Reise',
        'free_text': 'Zusätzliche Informationen zur Reise'
}