from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
from flask_mail import Message

from flask_cors import CORS
from flask_migrate import Migrate
import json
import os


app = Flask(__name__)
CORS(app)

# Funktion zum Laden der Konfiguration
def load_config():
    config_path = os.path.join(os.getcwd(), 'config', 'config.json')
    with open(config_path) as config_file:
        config = json.load(config_file)
    return config

# Konfiguration laden
config = load_config()

# .env-Datei laden
load_dotenv()

# Wartungsmodus abrufen (Standardwert ist False)
MAINTENANCE_MODE = os.getenv('MAINTENANCE_MODE', 'False') == 'True'

# Vor jeder Anfrage prüfen, ob der Wartungsmodus aktiviert ist
@app.before_request
def check_maintenance_mode():
    if MAINTENANCE_MODE:
        return jsonify({'error': 'Die Website befindet sich im Wartungsmodus. Bitte versuche es später erneut.'}), 503

app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class TestMail:
    def __init__(self):
        self.sent_messages = []

    def send(self, message: Message):
        """Anstatt die E-Mail zu senden, wird sie in einer Liste gespeichert."""
        self.sent_messages.append(message)

    def get_sent_messages(self):
        """Gibt alle gespeicherten Nachrichten zurück."""
        return self.sent_messages

'''
# Data for email service
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
'''

# Fake Mailserver with MailHog for testing
app.config["MAIL_SERVER"] = "localhost"
app.config["MAIL_PORT"] = 1025  # MailHog SMTP Port
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = None
app.config["MAIL_PASSWORD"] = None
app.config['MAIL_DEFAULT_SENDER'] = "noreply@example.com"


mail = Mail(app)

from routes import *


if __name__ == '__main__':
    app.run(debug=True)