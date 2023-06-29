"""Flask app configuration."""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class Config:
    """Set Flask configuration from environment variables."""

    FLASK_APP = 'app.py'
    # FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = "dev"

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Terga.ia.db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True