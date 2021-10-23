from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy

from spectree import SpecTree, SecurityScheme

from flask_jwt_extended import JWTManager

db = SQLAlchemy()
api = SpecTree(
    "flask",
    path="docs",
    title="Mini Feed",
    version="0.5.0",
    security_schemes=[
        SecurityScheme(
            name="api_key",
            data={"type": "apiKey", "name": "Authorization", "in": "header"},
        )
    ],
    security={"api_key": []},
)

jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)    

    jwt.init_app(app)
    db.init_app(app)

    from models import User

    @jwt.user_lookup_loader
    def user_load(token, data):
        current_user = User.query.filter_by(username=data["sub"]).first()

        return current_user

    from controllers import user_controller, posts_controller, auth_controller

    app.register_blueprint(auth_controller)
    app.register_blueprint(user_controller)
    app.register_blueprint(posts_controller)

    api.register(app)

    return app
