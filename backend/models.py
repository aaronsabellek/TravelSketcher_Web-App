from flask_login import UserMixin
from app import db

# Model für User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)  # Hinzufügen der E-Mail-Adresse
    password = db.Column(db.String(50), nullable=False)
    img_link = db.Column(db.String(200))

    # Beziehung zu Reisezielen
    destinations = db.relationship('Destination', backref='owner', lazy=True)
    # Beziehung zu Aktivitäten
    activities = db.relationship('Activity', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

# Model für Reiseziele
class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=True)
    img_link = db.Column(db.String(200), nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    tags = db.Column(db.String(200), nullable=True)
    position = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(50), nullable=True)
    months = db.Column(db.String(50), nullable=True)
    accomodation_link = db.Column(db.String(200), nullable=True)
    accomodation_price = db.Column(db.String(50), nullable=True)
    accomodation_text = db.Column(db.String(500), nullable=True)
    trip_duration = db.Column(db.String(50), nullable=True)
    trip_price = db.Column(db.String(50), nullable=True)
    trip_text = db.Column(db.String(500), nullable=True)
    free_text = db.Column(db.String(500), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activities = db.relationship('Activity', backref='destination', lazy=True)

    def __repr__(self):
        return f'<Destination {self.title} (Position: {self.position})>'

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    price = db.Column(db.String(50), nullable=True)
    activity_text = db.Column(db.String(500), nullable=True)
    number = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=True)
    web_link = db.Column(db.String(200), nullable=True)
    img_link = db.Column(db.String(200), nullable=True)
    tags = db.Column(db.String(200), nullable=True)
    trip_duration = db.Column(db.String(50), nullable=True)
    trip_price = db.Column(db.String(50), nullable=True)
    trip_text = db.Column(db.String(500), nullable=True)
    free_text = db.Column(db.String(500), nullable=True)

    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)

    def __repr__(self):
        return f'<Activity {self.title} for Destination {self.destination_id}>'