from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """Represents the user with his profile data"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    temp_email = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    longitude = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    currency = db.Column(db.String(20), nullable=False)
    is_email_verified = db.Column(db.Boolean, default=False)

    # Relationship to destinations
    destinations = db.relationship('Destination', backref='owner', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f'<User {self.username}>'


class Destination(db.Model):
    """Represents destinations of a user"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=True)
    img_link = db.Column(db.String(200), nullable=True)
    duration = db.Column(db.String(20), nullable=True)
    tags = db.Column(db.String(100), nullable=True)
    position = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=True)
    time = db.Column(db.String(20), nullable=True)
    accomodation_link = db.Column(db.String(200), nullable=True)
    pricing = db.Column(db.String(10), nullable=True)
    trip_pricing_flight = db.Column(db.String(10), nullable=True)
    trip_pricing_no_flight = db.Column(db.String(10), nullable=True)
    travel_duration_flight = db.Column(db.String(15), nullable=True)
    travel_duration_no_flight = db.Column(db.String(15), nullable=True)
    longitude = db.Column(db.String(20), nullable=True)
    latitude = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    free_text = db.Column(db.String(500), nullable=True)

    # Relationships to user and activities
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    activities = db.relationship('Activity', backref='destination', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f'<Destination {self.title} (Position: {self.position})>'


class Activity(db.Model):
    """Represents activities of a specific destination"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    pricing = db.Column(db.String(50), nullable=True)
    position = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=True)
    web_link = db.Column(db.String(200), nullable=True)
    img_link = db.Column(db.String(200), nullable=True)
    tags = db.Column(db.String(200), nullable=True)
    trip_duration = db.Column(db.String(50), nullable=True)
    trip_pricing = db.Column(db.String(50), nullable=True)
    longitude = db.Column(db.String(20), nullable=True)
    latitude = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    free_text = db.Column(db.String(500), nullable=True)

    # Relationship to destination
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'<Activity {self.title} for Destination {self.destination_id}>'