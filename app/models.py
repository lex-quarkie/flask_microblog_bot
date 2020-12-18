from datetime import datetime

from flask_login import UserMixin
from marshmallow import fields
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Binary,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app import db, ma

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    body = Column(String(1000), nullable=False)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Post #{self.id} by User #{self.user_id}"

    def likes(self):
        return db.session.query(Like).filter_by(post_id=self.id).count()


class PostSchema(ma.SQLAlchemyAutoSchema):
    likes_count = fields.Function(lambda obj: obj.likes())

    class Meta:
        model = Post


class User(UserMixin, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    posts = relationship("Post", backref="author", lazy="dynamic")
    hash = Column(Binary, nullable=False)

    def __repr__(self):
        return f"<User #{self.id} ({self.username})>"


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class UserLogEntry(Base):
    __tablename__ = "user_log_entries"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    method = Column(String)
    url = Column(String, index=True)


class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    post_id = Column("post_id", Integer, ForeignKey("posts.id"))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
user_schema = UserSchema()
