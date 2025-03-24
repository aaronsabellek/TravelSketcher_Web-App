from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from itsdangerous import URLSafeTimedSerializer

import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from flask_migrate import Migrate
import os

from app.errors import handle_exception, handle_http_exception, handle_db_error
from app.config import Config


# Flask Extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app(config_class=Config):
    """App Factory: Erstellt und konfiguriert die Flask-App"""
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(config_class)

    # Logger für die Entwicklungsumgebung
    if app.debug:
        # Logge auf der Konsole
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
    else:
        # Logge in eine Datei für die Produktionsumgebung
        handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=3)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

    # Erweiterungen mit der App verknüpfen
    app.config['SERIALIZER'] = URLSafeTimedSerializer(app.secret_key)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)  # Hier initialisieren!
    login_manager.login_view = 'login'
    mail.init_app(app)
    CORS(app)  # Falls CORS benötigt wird

    app.config['MAINTENANCE_MODE'] = os.getenv('MAINTENANCE_MODE', False) == 'True'
    @app.before_request
    def check_maintenance_mode():
        if app.config['MAINTENANCE_MODE']:
            return jsonify({'error': 'Die Website befindet sich im Wartungsmodus. Bitte versuche es später erneut.'}), 503

    app.errorhandler(Exception)(handle_exception)
    app.errorhandler(HTTPException)(handle_http_exception)
    app.errorhandler(SQLAlchemyError)(handle_db_error)

    # Blueprints registrieren
    from app.routes import register_blueprints
    register_blueprints(app)

    return app
