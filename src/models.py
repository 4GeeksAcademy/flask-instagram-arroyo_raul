from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from typing import List


db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    secondname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")
    followers: Mapped[List["Follower"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "secondname": self.secondname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="followers")

    def serialie(self):
        return{
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }

    
class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    
class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(SqlEnum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return{
            "id": self.id,
            "type": self.type.value,
            "url": self.url,
            "post_id": self.post_id
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[List["Media"]] = relationship(back_populates="post")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(255))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="comments")

    def serialize(self):
        return{
            "id": self.id,
            "comment_text": self.comment_text,
            "post_id": self.post_id,
            "user_id": self.user_id
        }