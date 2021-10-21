from main import app
from factory import db

from models import Post, User

from datetime import datetime

with app.app_context():
    user = User.query.first()

    print(user, user.posts.all())

    # for post in user.posts:
    #     print(post.created, post.text)

    # post = Post(text="Hello Feed", author=user)
    # db.session.add(post)
    # db.session.commit()

