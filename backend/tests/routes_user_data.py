from tests.helping_variables import (
    dummy_data,
    user,
    second_user,
    username,
    email,
    password,
    city,
    longitude,
    latitude,
    country,
    currency,
    is_email_verified
)


updated_profile= {
    'username': 'new_username',
    'city': city,
    'longitude': longitude,
    'latitude': latitude,
    'country': country,
    'currency': currency
}

edit_data = [
    # Missing value
    {**updated_profile, 'city': '', 'expected_status': 400, 'expected_message': 'city not found!'},
    # Username already exists
    {**updated_profile, 'username': 'second_user', 'expected_status': 400, 'expected_message': 'This username already exists!'},

    # Successfull test case
    {**updated_profile, 'expected_status': 200, 'expected_message': 'Updated User successfully!'},
    # Successfull test case with unallowed field
    {**updated_profile, 'password': 'unallowed_password123!', 'expected_status': 200, 'expected_message': 'Updated User successfully!'},
]

