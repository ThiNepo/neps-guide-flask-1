from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from controllers import demo_controller, user_controller

    app.register_blueprint(demo_controller)
    app.register_blueprint(user_controller)

    return app
