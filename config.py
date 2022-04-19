from os import environ

class Config:
    """Set Flask configuration vars from .env file."""

    # General
    TESTING = environ.get("TESTING")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
