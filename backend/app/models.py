import uuid

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    """Represents the user with his profile data"""

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    temp_email = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    is_email_verified = db.Column(db.Boolean, default=False)

    # Relationship to destinations
    destinations = db.relationship('Destination', backref='owner', lazy=True, cascade='all, delete')

    def __repr__(self):
        return f'<User {self.username}>'


class Destination(db.Model):
    """Represents destinations of a user"""

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=True)
    img_link = db.Column(db.String(500), nullable=True)
    tags = db.Column(db.String(200), nullable=True)
    position = db.Column(db.Integer, nullable=False)
    free_text = db.Column(db.String(1000), nullable=True)

    # Relationships to user and activities
    user_id = db.Column(db.String(36), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    activities = db.relationship('Activity', backref='destination', lazy=True, cascade='all, delete')

    def __repr__(self):
        return f'<Destination {self.title} (Position: {self.position})>'


class Activity(db.Model):
    """Represents activities of a specific destination"""

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(50), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    web_link = db.Column(db.String(500), nullable=True)
    img_link = db.Column(db.String(500), nullable=True)
    tags = db.Column(db.String(200), nullable=True)
    free_text = db.Column(db.String(1000), nullable=True)

    # Relationship to destination
    destination_id = db.Column(db.String(36), db.ForeignKey('destination.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<Activity {self.title} for Destination {self.destination_id}>'