from app.models import User, Destination, Activity


def test_user_creation(setup_database):
    """Test: Creation of user"""

    user = User.query.filter_by(username='test_user').first()

    assert user is not None
    assert isinstance(user.id, str), f'Expected ID to be a string, but got {type(user.id)}'
    assert user.email == 'test_user@example.com'
    assert user.city == 'Leipzig'
    assert user.currency == 'EUR'


def test_destination_creation(setup_database):
    """Test: Creation of destination"""

    destination = Destination.query.filter_by(title='Paris').first()

    assert destination is not None
    assert isinstance(destination.id, str), f'Expected ID to be a string, but got {type(destination.id)}'
    assert destination.country == 'France'


def test_activity_creation(setup_database):
    """Test: Creation of activities"""

    activity = Activity.query.filter_by(title='Visit the Eiffel Tower').first()

    assert activity is not None
    assert isinstance(activity.id, str), f'Expected ID to be a string, but got {type(activity.id)}'
    assert activity.country == 'France'