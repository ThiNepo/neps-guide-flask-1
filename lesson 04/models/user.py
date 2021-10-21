from datetime import datetime
from factory import db
from typing import List, Union
from pydantic import BaseModel


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), index=True)
    birthday = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class OrmBase(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UserResponse(OrmBase):
    username: str
    email: str
    birthday: datetime = None


class UserCreate(BaseModel):
    username: str
    email: str
    birthday: datetime = None


class UserResponseList(BaseModel):
    __root__: List[UserResponse]
