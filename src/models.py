from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum


db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    secondname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "secondname": self.secondname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    
class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(SqlEnum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "type": self.type.value,
            "url": self.url
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def serialize(self):
        return {
            "id": self.id
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(255))

    def serialize(self):
        return{
            "id": self.id,
            "comment_text": self.comment_text
        }