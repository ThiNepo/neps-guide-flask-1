from flask import Blueprint, jsonify
from flask.globals import request

import json

from models.user import User, UserResponseList

from factory import db, api

from datetime import datetime

from typing import List
from spectree import Response

from models.user import UserResponse

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")


@user_controller.route("/", methods=["GET"])
@api.validate(resp=Response(HTTP_200=UserResponseList), tags=["users"])
def get_users():
    """
    Get all users
    """

    users = User.query.all()

    response = UserResponseList(
        __root__=[UserResponse.from_orm(user).dict() for user in users]
    ).json()

    return jsonify(json.loads(response))


@user_controller.route("/<int:user_id>")
@api.validate(resp=Response(HTTP_200=UserResponse, HTTP_404=None), tags=["users"])
def get_user(user_id):
    """
    Get a specified user
    """

    user = User.query.get(user_id)

    if user is None:
        return {"msg": f"There is no user with id {user_id}"}, 404

    response = UserResponse.from_orm(user).json()

    return json.loads(response)


@user_controller.route("/<int:user_id>", methods=["PUT"])
def put_user(user_id):
    """
    Update an user
    """

    user = User.query.get(user_id)

    if user is None:
        return {"msg": f"There is no user with id {user_id}"}, 404

    data = request.json

    # Update user

    user.username = data["username"]
    user.email = data["email"]
    user.birthday = data["birthday"]

    db.session.commit()

    return {"msg": "User was updated."}


@user_controller.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete an user
    """

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return {"msg": "User deleted from the database."}, 200


@user_controller.route("/", methods=["POST"])
def post_user():
    """
    Create an user
    """
    data = request.json

    user = User(username=data["username"], email=data["email"])

    db.session.add(user)
    db.session.commit()

    return {"msg": "User created successfully."}, 201
