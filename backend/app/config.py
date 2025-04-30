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

    # Initialize maintenance mode
    MAINTENANCE_MODE = os.getenv('MAINTENANCE_MODE', 'False').lower() == 'true'
    MAINTENANCE_MESSAGE= os.getenv(
        'MAINTENANCE_MESSAGE',
        'This Website is currently in Maintainance mode. Please try again later.'
    )

    # Initialize SQLAlchemy track modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookie Management
    SESSION_COOKIE_SAMESITE= 'Lax'
    SESSION_COOKIE_SECURE= False

    # Initlialize mailserver data from MailHog for testing
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = 'noreply@example.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False

    # Unsplash access key for images
    UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')


class DevelopmentConfig(Config):
    """Flask configuration class for development"""

    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'
    MAIL_SUPPRESS_SEND = False
    CORS_ORIGINS = ["http://localhost:3000"]

    # Initialize local development database with SQLAlchemy
    DATABASE_URI_DEV = os.getenv('DATABASE_URI_DEV')

    #if DATABASE_URI_DEV is None:
    #    raise ValueError('DATABASE_URI_DEV is not set in the .env file.')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI_DEV')


class TestingConfig(Config):
    """Flask configuration class for testing"""

    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = False
    CORS_ORIGINS = ["http://localhost:3000"]

    # Initialize memory database from SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Flask configuration class for production"""

    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    LOG_LEVEL = 'WARNING'

    # Cookie Management
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'None'

    # CORS
    CORS_ORIGINS = ["https://travelsketcher.onrender.com"]

    # Initialize production database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI_PROD')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError('DATABASE_URI not set in .env')

    # Initialize production mail server
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'

    if not all([MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER]):
        raise ValueError('Production mail configuration incomplete.')

