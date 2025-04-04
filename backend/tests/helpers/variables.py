from tests.helpers.dummy_data import dummy_data

# Standard URL
url = 'http://127.0.0.1:5000'

# Mailhog URLs
mailhog_v2 = 'http://localhost:8025/api/v2/messages'
mailhog_v1 = 'http://localhost:8025/api/v1/messages'

# Variables for main user
user = dummy_data['user']

user_id = user['id']
username = user['username']
email = user['email']
password = user['password']
city = user['city']
longitude = user['longitude']
latitude = user['latitude']
country = user['country']
currency = user['currency']
is_email_verified = user['is_email_verified']

# Variables for main user destinations
destinations = dummy_data['destinations']

dest_main_id = destinations[0]['id']
dest_2_id = destinations[1]['id']
dest_3_id = destinations[2]['id']

# Variables for main user activities
activities = dummy_data['destinations'][0]['activities']

act_main_id = activities[0]['id']
act_2_id = activities[1]['id']
act_3_id = activities[2]['id']
act_4_id = activities[3]['id']
act_5_id = activities[4]['id']

# Variables for secondary user and his entries
second_user = dummy_data['second_user']

user_second_id = second_user['id'] # ID
dest_second_user_id = dummy_data['second_destinations'][0]['id'] # Destination
act_second_user_id = dummy_data['second_destinations'][0]['activities'][0]['id'] # Activity

# Variable for wrong id
wrong_id = '11111111-1111-1111-1111-111111111111'

# Base data for registration
registration_base_data = {
        **user,
        'username': 'test_user_registration',
        'email': 'registration@example.com',
}

# Login data with username
login_data_username = {
    'identifier': user['username'],
    'password': user['password']
}

