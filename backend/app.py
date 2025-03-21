from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
from flask_mail import Message
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from errors import handle_exception, handle_http_exception, handle_db_error

from flask_cors import CORS
from flask_migrate import Migrate
import os


# Initialize app
app = Flask(__name__)
CORS(app)

# Load configuration from .env
load_dotenv()

# Initialize maintainance mode
MAINTENANCE_MODE = os.getenv('MAINTENANCE_MODE', 'False') == 'True'
@app.before_request
def check_maintenance_mode():
    if MAINTENANCE_MODE:
        return jsonify({'error': 'Die Website befindet sich im Wartungsmodus. Bitte versuche es später erneut.'}), 503

# Initialize SQLAlchemy
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize error handlers
app.errorhandler(Exception)(handle_exception)
app.errorhandler(HTTPException)(handle_http_exception)
app.errorhandler(SQLAlchemyError)(handle_db_error)

# Initialize db
db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initlialize mailserver data
MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
MAIL_PORT = os.getenv('MAIL_PORT', 1025)
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', False)
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', False)
MAIL_USERNAME = os.getenv('MAIL_USERNAME', None)
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', None)
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@example.com')

mail = Mail(app)


from routes import *


if __name__ == '__main__':
    #app.run(debug=True)
    debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
    app.debug = debug
    app.run(debug=debug)
