from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv

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

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

from routes import *


if __name__ == '__main__':
    app.run(debug=True)