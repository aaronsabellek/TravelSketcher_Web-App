import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Flask Konfigurationsklasse"""
    SECRET_KEY = os.getenv("SECRET_KEY")
    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY is not set! Insert the .env file.")

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    if SQLALCHEMY_DATABASE_URI is None:
        raise ValueError("DATABASE_URL is not set! Insert the .env file.")

    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() == "true"

    MAINTENANCE_MODE = os.getenv("MAINTENANCE_MODE", "False").lower() == "true"

    # Initlialize mailserver data from .env (MailHog for testing purpose)
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME') or None
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') or None
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    if MAIL_SERVER is None or MAIL_PORT is None or MAIL_USERNAME is None or MAIL_PASSWORD is None or MAIL_DEFAULT_SENDER is None:
        raise ValueError("E-Mail-configuration is missing in the .env-file!")

    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', False) == 'True'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', False) == 'True'

