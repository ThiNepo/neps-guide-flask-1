from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy

from spectree import SpecTree

db = SQLAlchemy()
api = SpecTree("flask")


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from controllers import user_controller

    app.register_blueprint(user_controller)

    api.register(app)

    return app
