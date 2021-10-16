from datetime import datetime
from factory import db
from typing import List
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), index=True)
    birthday = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


UserResponse = sqlalchemy_to_pydantic(User, exclude=["created_at"])


class UserResponseList(BaseModel):
    __root__: List[UserResponse]
