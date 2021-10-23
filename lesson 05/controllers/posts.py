from datetime import datetime
import json
from factory import api, db
from flask import Blueprint, request, jsonify
from models.post import PostCreate, Post, PostResponse, PostResponseList
from spectree import Response
from utils.responses import DefaultResponse


posts_controller = Blueprint("posts_controller", __name__, url_prefix="/posts")


# Post (Create)
@posts_controller.route("/", methods=["POST"])
@api.validate(json=PostCreate, resp=Response(HTTP_201=DefaultResponse), tags=["posts"])
def create():
    """Create post"""

    data = request.json

    post = Post(text=data["text"], author_id=data["author_id"])

    db.session.add(post)
    db.session.commit()

    return {"msg": "Post created"}


# Get all
@posts_controller.route("/", methods=["GET"])
@api.validate(resp=Response(HTTP_200=PostResponseList), tags=["posts"])
def get_all():
    """Get all posts"""

    posts = Post.query.all()

    response = PostResponseList(
        __root__=[PostResponse.from_orm(post).dict() for post in posts]
    ).json()

    return jsonify(json.loads(response))


# Get one
@posts_controller.route("/<int:post_id>", methods=["GET"])
@api.validate(
    resp=Response(HTTP_200=PostResponse, HTTP_404=DefaultResponse), tags=["posts"]
)
def get_one(post_id):
    """Get one post"""

    post = Post.query.get(post_id)

    if post:
        response = PostResponse.from_orm(post).json()

        return json.loads(response)

    return {"msg": "This post does not exists."}, 404


# Update
@posts_controller.route("/<int:post_id>", methods=["PUT"])
@api.validate(
    json=PostResponse,
    resp=Response(HTTP_200=DefaultResponse, HTTP_404=DefaultResponse),
    tags=["posts"],
)
def update(post_id):
    """Update a post"""

    post = Post.query.get(post_id)

    if post is None:
        return {"msg": "This post does not exists."}, 404

    data = request.json

    post.text = data["text"]
    post.author_id = data["author_id"]
    # post.created = datetime.fromisoformat(data["created"])

    db.session.commit()

    return {"msg": "The post was updated."}


# Delete
@posts_controller.route("/<int:post_id>", methods=["DELETE"])
@api.validate(
    resp=Response(HTTP_200=DefaultResponse, HTTP_404=DefaultResponse),
    tags=["posts"],
)
def delete(post_id):
    """Delete a post"""

    post = Post.query.get(post_id)

    if post is None:
        return {"msg": "This post does not exists."}, 404

    db.session.delete(post)
    db.session.commit()

    return {"msg": "The post was deleted"}
