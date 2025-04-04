import os

from dotenv import load_dotenv

# Load data from .env file
load_dotenv()


class Config:
    """Flask configuration class"""

    # Initialize secret key
    SECRET_KEY = os.getenv('SECRET_KEY')
    if SECRET_KEY is None:
        raise ValueError('SECRET_KEY is not set! Insert the .env file.')

    # Initialize database with SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    if SQLALCHEMY_DATABASE_URI is None:
        raise ValueError('DATABASE_URL is not set! Insert the .env file.')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Initialize maintenance mode
    MAINTENANCE_MODE = os.getenv('MAINTENANCE_MODE', 'False').lower() == 'true'
    MAINTENANCE_MESSAGE= os.getenv('MAINTENANCE_MESSAGE', 'This Website is currently in Maintainance mode. Please try again later.')

    # Initlialize mailserver data (MailHog for testing purpose)
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME') or None
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') or None
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    if MAIL_SERVER is None or MAIL_PORT is None or MAIL_USERNAME is None or MAIL_PASSWORD is None or MAIL_DEFAULT_SENDER is None:
        raise ValueError("E-Mail-configuration is missing in the .env-file!")

    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', False) == 'True'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', False) == 'True'


class DevelopmentConfig(Config):
    """Flask configuration class for development"""

    DEBUG = True
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    """Flask configuration class for testing"""

    TESTING = True


class ProductionConfig(Config):
    """Flask configuration class for production"""

    DEBUG = False
    SESSION_COOKIE_SECURE = True

