from flask import Flask
from config import Config

from controllers import demo_controller


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(demo_controller)

    return app
