from tests.helping_variables import (
    user,
    username,
    email,
    password,
    registration_base_data
)


# Test data for registration
registration_data = [
    # Empty required field
    {**registration_base_data, 'country': '', 'expected_status': 400, 'expected_message': 'Field(s) missing!'},
    # '@' in username
    {**registration_base_data, 'username': 'test_user@registration', 'expected_status': 400, 'expected_message': "'@' in username is not allowed!"},
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
    {**registration_base_data, 'username': username, 'expected_status': 400, 'expected_message': 'Username is already taken!'},
    # Existing email
    {**registration_base_data, 'email': email, 'expected_status': 400, 'expected_message': 'Email is already taken!'},

    # Successfull test case
    {**registration_base_data, 'expected_status': 201, 'expected_message': 'Registration was successfull! A confirmation link has been sent.'}
]

# Test data for verification
verification_data = [
    # Email does not exist in db
    {'email': 'wrong_email@test-com', 'expected_status': 404, 'expected_message': 'User not found!'},
    # User is already verified
    {'email': email, 'is_email_verified': True, 'expected_status': 200, 'expected_message': 'E-Mail has already been confirmed!'},
    # Token is wrong
    {'email': email, 'invalid_token': True, 'expected_status': 400, 'expected_message': 'Invalid or expired token!'},

    # Successfull test case
    {'email': email, 'expected_status': 200, 'expected_message': 'E-Mail confirmed successfully!'}
]

# Test data for resending verification mail
resend_verification_data = [
    # User does not exist in db
    {'email': 'non_existing_email', 'expected_status': 404, 'expected_message': 'User not found!'},
    # User is already verified
    {'email': email, 'expected_status': 200, 'expected_message': 'E-Mail is already verified!'},

    # Succesfull test case
    {'email': registration_base_data['email'], 'expected_status': 200, 'expected_message': 'New verification link has been sent!'}
]

# Test data for login
login_data = [
    # User is already logged in
    {'identifier': username, 'password': password, 'already_logged': True, 'expected_status': 200, 'expected_message': 'You are logged in already'},
    # Password is missing
    {'identifier': username, 'expected_status': 400, 'expected_message': 'Username or password is missing!'},
    # Identifier does not exist in db
    {'identifier': 'wrong_identifier', 'password': password, 'expected_status': 404, 'expected_message': 'User not found!'},
    # Incorect password
    {'identifier': username, 'password': 'wrong_password', 'expected_status': 400, 'expected_message': 'Wrong password!'},
    # Email has not been confirmed yet
    {'identifier': email, 'password': password, 'already_confirmed': True, 'expected_status': 403, 'expected_message': 'E-Mail has not been confirmed yet!'},

    # Successfull test case with username
    {'identifier': username, 'password': password, 'expected_status': 200, 'expected_message': 'Login successfull!'},
    # Successfull test case with email
    {'identifier': email, 'password': password, 'expected_status': 200, 'expected_message': 'Login successfull!'}
]

