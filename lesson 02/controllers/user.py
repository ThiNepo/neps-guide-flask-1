from flask import Blueprint, jsonify
from flask.globals import request

from models.user import User

from factory import db

from datetime import datetime

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")


@user_controller.route("/", methods=["GET"])
def get_users():

    users = User.query.all()

    return jsonify(
        [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "birthday": user.birthday,
            }
            for user in users
        ]
    )


@user_controller.route("/<int:user_id>")
def get_user(user_id):

    user = User.query.get(user_id)

    if user is None:
        return {"msg": f"There is no user with id {user_id}"}, 404

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "birthday": user.birthday,
    }


@user_controller.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return {"msg": "User deleted from the database."}, 200


@user_controller.route("/", methods=["POST"])
def post_user():
    form = request.form

    user = User(
        username=form["username"],
        email=form["email"],
        birthday=datetime.fromisoformat(form["birthdate"]),
    )

    db.session.add(user)
    db.session.commit()

    return {"msg": "User created successfully."}, 201
