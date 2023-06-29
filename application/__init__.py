from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .model.sse.TergaClient import TergaClient

db = SQLAlchemy()
tergaClient = TergaClient()


"""Construct the core app object."""
app = Flask(__name__, instance_relative_config=False)

# Application Configuration
app.config.from_object('config.Config')

with app.app_context():
    # Initialize Plugins
    db.init_app(app)

    from .routes import index,pytorch,parallelManager,database
    from . import auth

    # Create Database Models
    db.create_all()