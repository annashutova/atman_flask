"""Flask app configuration."""
from os import getenv
from dotenv import load_dotenv


load_dotenv()


class Config(object):
    """Sets default config variables."""
    SECRET_KEY = getenv('SECRET_KEY')
    SESSION_COOKIE_NAME = getenv('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = getenv('MAIL_DEFAULT_SENDER')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')


class DevConfig(Config):
    """Sets development config variables."""
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    """Sets production config variables."""
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

DEFAULT_STRING_VALUE = 100
PASSWORD_LENGTH = 300
