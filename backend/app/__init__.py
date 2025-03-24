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
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from flask_migrate import Migrate

from app.errors import handle_exception, handle_http_exception, handle_db_error, page_not_found, method_not_allowed
from app.config import DevelopmentConfig, ProductionConfig


# Flask Extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app(config_class=DevelopmentConfig):
    """App Factory: Erstellt und konfiguriert die Flask-App"""
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(config_class)

    # Einschränken der Ausgabe im Productionmode
    app.config['PROPAGATE_EXCEPTIONS'] = app.config['DEBUG']

    # Erzwungene Nutzung von HTTPS in der Produktion
    if not app.debug:
        Talisman(app, force_https=True)

    # Sichere Cookies für Sessions in der Produktion
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # oder 'Lax' je nach Bedarf

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
        if not any(isinstance(h, RotatingFileHandler) for h in app.logger.handlers):
            handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=3)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            app.logger.addHandler(handler)

    @app.before_request
    def log_request_info():
        current_app.logger.info(f"Neue Anfrage: {request.method} {request.url}")

    # Erweiterungen mit der App verknüpfen
    app.config['SERIALIZER'] = URLSafeTimedSerializer(app.secret_key)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)  # Hier initialisieren!
    login_manager.login_view = 'login'
    mail.init_app(app)
    CORS(app)  # Falls CORS benötigt wird

    app.config['MAINTENANCE_MODE'] = os.getenv('MAINTENANCE_MODE', False) == 'True'
    app.config['MAINTENANCE_MESSAGE'] = os.getenv('MAINTENANCE_MESSAGE', 'This Website is currently in Maintainance mode. Please try again later.')
    @app.before_request
    def check_maintenance_mode():
        if app.config['MAINTENANCE_MODE']:
            return jsonify({'error': app.config['MAINTAINANCE_MESSAGE']}), 503

    app.errorhandler(404)(page_not_found)
    app.errorhandler(405)(method_not_allowed)
    app.errorhandler(Exception)(handle_exception)
    app.errorhandler(HTTPException)(handle_http_exception)
    app.errorhandler(SQLAlchemyError)(handle_db_error)

    # Blueprints registrieren
    from app.routes import register_blueprints
    register_blueprints(app)

    return app
