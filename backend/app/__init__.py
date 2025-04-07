import logging
import os

from flask import Flask, jsonify, current_app, request
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from itsdangerous import URLSafeTimedSerializer
from flask_cors import CORS
from flask_migrate import Migrate
from logging.handlers import RotatingFileHandler

from app.config import DevelopmentConfig, TestingConfig, ProductionConfig
from app.errors import (
    handle_exception,
    handle_http_exception,
    handle_db_error, page_not_found,
    method_not_allowed
)

# Flask Extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app(config_class=None):
    """App Factory: Creates and configures Flask-App"""

    ### 1. Initialize Flask App ###

    app = Flask(__name__)

    ### 2. Load environment variables and configuration ###

    # Load data from .env
    load_dotenv()

    # Load Flask environment and configuration class
    if config_class is None:
        env = os.getenv('FLASK_ENV', 'development') # standard mode
        if env == 'production':
            app.config.from_object(ProductionConfig)
        elif env == 'testing':
            app.config.from_object(TestingConfig)
        else:
            app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(config_class)

    ### 3. Logging ###

    # Set up directory for logs
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Logging INFO to console in development mode
    if os.getenv('FLASK_ENV') == 'development':
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

    # Logging WARNING to rotating files and console in production mode
    elif os.getenv('FLASK_ENV') == 'production':
        handler = RotatingFileHandler(
            os.path.join(log_dir, 'app.log'),
            maxBytes=10240,
            backupCount=3
        )
        handler.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)

    ### 4. Security and HTTPS configuration ###

    # Allow error reports when DEBUG == True
    app.config['PROPAGATE_EXCEPTIONS'] = app.config['DEBUG']

    # Force use of HTTPS in production
    if os.getenv('FLASK_ENV') == 'production':
        Talisman(app, force_https=True)

    # Secure cookies for sessions in production
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

    ### 5. Initialize Flask extensions ###

    # Log incoming requests with method and URL before processing
    @app.before_request
    def log_request_info():
        current_app.logger.info(f'New request: {request.method} {request.url}')

    # Initialize the URLSafeTimedSerializer
    app.config['SERIALIZER'] = URLSafeTimedSerializer(app.secret_key)

    # Bind SQLAlchemy database object to the app
    db.init_app(app)

    # Set up Flask-Migrate extension
    migrate.init_app(app, db)

    # Initialize the Flask-Login extension
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Initialize Flask Mail extension
    mail.init_app(app)

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)

    ### 6. Maintenance mode and error handling ###

    # Initialize maintenance mode
    app.config['MAINTENANCE_MODE'] = os.getenv('MAINTENANCE_MODE', False) == 'True'
    app.config['MAINTENANCE_MESSAGE'] = os.getenv('MAINTENANCE_MESSAGE', 'This Website is currently in Maintainance mode. Please try again later.')
    @app.before_request
    def check_maintenance_mode():
        if app.config['MAINTENANCE_MODE']:
            return jsonify({'error': app.config['MAINTAINANCE_MESSAGE']}), 503

    # Initialize error handlers
    app.errorhandler(404)(page_not_found)
    app.errorhandler(405)(method_not_allowed)
    app.errorhandler(Exception)(handle_exception)
    app.errorhandler(HTTPException)(handle_http_exception)
    app.errorhandler(SQLAlchemyError)(handle_db_error)

    ### 7. Register blueprints ###

    from app.routes import register_blueprints
    register_blueprints(app)

    return app

