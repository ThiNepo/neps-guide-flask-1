from flask import Blueprint, jsonify
from flask.globals import request

import json

from pydantic.main import BaseModel

from models.user import User, UserCreate, UserResponseList

from factory import db, api

from datetime import datetime

from typing import List
from spectree import Response

from models.user import UserResponse, UserCreate

from utils.responses import DefaultResponse

from flask_jwt_extended import jwt_required, current_user

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")


@user_controller.route("/", methods=["GET"])
@api.validate(resp=Response(HTTP_200=UserResponseList), tags=["users"])
@jwt_required()
def get_users():
    """
    Get all users
    """

    print(request.headers)

    users = User.query.all()

    response = UserResponseList(
        __root__=[UserResponse.from_orm(user).dict() for user in users]
    ).json()

    return jsonify(json.loads(response))


@user_controller.route("/<int:user_id>")
@api.validate(resp=Response(HTTP_200=UserResponse, HTTP_404=None), tags=["users"])
@jwt_required()
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
@api.validate(
    json=UserResponse,
    resp=Response(HTTP_200=DefaultResponse),
    tags=["users"],
)
@jwt_required()
def put_user(user_id):
    """
    Update an user
    """

    user = User.query.get(user_id)

    if user is None:
        return {"msg": f"There is no user with id {user_id}"}, 404

    if user.id != current_user.id:
        return {"msg": "You can only change you own information."}, 403

    data = request.json

    # Update user

    user.username = data["username"]
    user.email = data["email"]

    if data["birthday"]:
        if data["birthday"].endswith("Z"):
            data["birthday"] = data["birthday"][:-1]

        user.birthday = datetime.fromisoformat(data["birthday"])

    db.session.commit()

    return {"msg": "User was updated."}


@user_controller.route("/<int:user_id>", methods=["DELETE"])
@api.validate(resp=Response(HTTP_200=DefaultResponse), tags=["users"])
@jwt_required()
def delete_user(user_id):
    """
    Delete an user
    """

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return {"msg": "User deleted from the database."}, 200


@user_controller.route("/", methods=["POST"])
@api.validate(json=UserCreate, resp=Response(HTTP_201=DefaultResponse), tags=["users"])
def post_user():
    """
    Create an user
    """
    data = request.json

    user = User(
        username=data["username"], email=data["email"], password=data["password"]
    )

    if "birthday" in data and data["birthday"]:
        if data["birthday"].endswith("Z"):
            data["birthday"] = data["birthday"][:-1]

        user.birthday = datetime.fromisoformat(data["birthday"])

    db.session.add(user)
    db.session.commit()

    return {"msg": "User created successfully."}, 201
