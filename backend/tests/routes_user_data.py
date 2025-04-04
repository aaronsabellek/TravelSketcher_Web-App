from tests.dummy_data import dummy_data
from tests.helping_variables import (
    email,
    city,
    longitude,
    latitude,
    country,
    currency
)

# Variables for user tests
new_password = 'New_password_123!'
wrong_password = 'newpassword123'
new_email= 'new_email@mail.com'

# Base data to edit user profile
updated_profile= {
    'username': 'new_username',
    'city': city,
    'longitude': longitude,
    'latitude': latitude,
    'country': country,
    'currency': currency
}

# Test data to edit user profile
edit_data = [
    # Missing value
    {**updated_profile, 'city': '', 'expected_status': 400, 'expected_message': 'city not found!'},
    # Username already exists
    {**updated_profile, 'username': 'second_user', 'expected_status': 400, 'expected_message': 'This username already exists!'},
    # '@' in username
    {**updated_profile, 'username': 'new@user', 'expected_status': 400, 'expected_message': "'@' in username is not allowed!"},

    # Successfull test case
    {**updated_profile, 'expected_status': 200, 'expected_message': 'Updated User successfully!'},
    # Successfull test case with unallowed field
    {**updated_profile, 'password': 'unallowed_password123!', 'expected_status': 200, 'expected_message': 'Updated User successfully!'},
]

# Test data to edit user email
edit_email = [
    # No Email
    {'expected_status': 400, 'expected_message': 'No E-Mail found!'},
    # No Email input
    {'email': '', 'expected_status': 400, 'expected_message': 'No E-Mail found!'},
    # Wrong email format
    {'email': 'new_email.com', 'expected_status': 400, 'expected_message': 'Wrong Email format!'},
    # Email already exists in db
    {'email': dummy_data['second_user']['email'], 'expected_status': 400, 'expected_message': 'E-Mail is already taken!'},

    # Successfull test case
    {'email': new_email, 'expected_status': 200, 'expected_message': 'Verification e-mail has been sent.'}
]

# Test data to verify new email of user
reset_email= [
    # Wrong email adress
    {'email': email, 'expected_status': 404, 'expected_message': 'Request to edit email not found'},

    # Successfull test case
    {'email': new_email, 'expected_status': 200, 'expected_message': 'Email verification successful!'}
]

# Test data to edit password of user
edit_password = [
    # Password missing
    {'new_password_1': new_password, 'expected_status': 400, 'expected_message': 'Password missing!'},
    # Passwords do not match
    {'new_password_1': new_password, 'new_password_2': 'not_new_password123!', 'expected_status': 400, 'expected_message': 'Passwords do not match!'},
    # Password does not fit the requirements
    {'new_password_1': wrong_password, 'new_password_2': wrong_password, 'expected_status': 400, 'expected_message': 'Passwort has to have at least one special character!'},

    # Successfull test case
    {'new_password_1': new_password, 'new_password_2': new_password, 'expected_status': 200, 'expected_message': 'Password updated successfully!'}
]

# Test data to request password reset
request_password_reset = [
    # Missing email
    {'expected_status': 400, 'expected_message': 'Email missing!'},
    # Non existing mail
    {'email': 'non_existing@mail.com', 'expected_status': 404, 'expected_message': 'E-Mail not found!'},

    # Successfull test case
    {'email': email, 'expected_status': 200, 'expected_message': 'A reset link has been sent.'}
]

# Test data to reset password
reset_password = [
    # Invalid token
    {'invalid_token': True, 'new_password_1': new_password, 'new_password_2': new_password, 'expected_status': 400, 'expected_message': 'Invalid or expired token'},
    # Password does not fit the requirements
    {'new_password_1': wrong_password, 'new_password_2': wrong_password, 'expected_status': 400, 'expected_message': 'Passwort has to have at least one special character!'},
    # Passwords do not match each other
    {'new_password_1': new_password, 'new_password_2': 'another_password123!', 'expected_status': 400, 'expected_message': 'Passwords do not match!'},

    # Successfull test case
    {'new_password_1': new_password, 'new_password_2': new_password, 'expected_status': 200, 'expected_message': 'Password updated successfully!'}
]

