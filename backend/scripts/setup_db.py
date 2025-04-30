from app import create_app, db
from app.config import DevelopmentConfig, TestingConfig, ProductionConfig
from tests.helpers.functions import create_user, create_destinations_and_activities
from tests.helpers.variables import (
    user,
    destinations,
)

app = create_app(DevelopmentConfig)


def setup():
    """Creates database with dummy data"""

    with app.app_context():

        print('Seeding dummy data...')

        # Create new database
        db.create_all()
        db.drop_all()
        db.create_all()

        # Create main user and secondary user
        main_user = create_user(db, user)

        # Create destinations and activities for users
        create_destinations_and_activities(db, destinations, main_user)

        # Commit changes in databae
        db.session.commit()
        print('Done.')


if __name__ == '__main__':
    setup()

