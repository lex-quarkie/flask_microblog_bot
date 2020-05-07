from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(UserMixin, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    posts = relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User #{self.id} ({self.username})>'


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    body = Column(String(140), nullable=False)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f'<Post #{self.id} by User #{self.user_id}'
