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

DEFAULT_STRING_VALUE = 50
PASSWORD_LENGTH = 300
