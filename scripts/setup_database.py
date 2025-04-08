from backend.app import create_app, db
from backend.app.config import DevelopmentConfig
from backend.tests.helpers.functions import create_user, create_destinations_and_activities
from backend.tests.helpers.variables import (
    user,
    second_user,
    destinations,
    second_destinations
)

app = create_app(DevelopmentConfig)


def setup():
    """Creates database with dummy data"""

    with app.app_context():

        print('Seeding dummy data...')

        # Create new database
        db.drop_all()
        db.create_all()

        # Create main user and secondary user
        main_user = create_user(db, user)
        secondary_user = create_user(db, second_user)

        # Create destinations and activities for users
        create_destinations_and_activities(db, destinations, main_user)
        create_destinations_and_activities(db, second_destinations, secondary_user)

        # Commit changes in databae
        db.session.commit()
        print('Done.')


if __name__ == '__main__':
    setup()

