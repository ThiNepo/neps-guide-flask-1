from main import app
from factory import db

from models import Post, User

from datetime import datetime

with app.app_context():
    users = User.query.all()

    for index, user in enumerate(users):
        user.password = f"secret{index}"        

    db.session.commit()

    # for post in user.posts:
    #     print(post.created, post.text)

    # post = Post(text="Hello Feed", author=user)
    # db.session.add(post)
    # db.session.commit()
