import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer

from database.base import Base, Session
from sqlalchemy.orm import relationship
from models.user import User
from flask import jsonify


class Post(Base):
    __tablename__ = "post"
    # Attributes :
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=True)
    body = Column(String, nullable=False)
    # Relations : 
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", foreign_keys=[user_id], uselist=False)

    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id

    def __repr__(self):
        return "<Post_id = {}>".format(self.id)
    
    def __str__(self):
        return self.__repr__()

    def to_json(self):
        print(type(self.user.to_json()))
        return {
                "user": self.user.to_json(),
                "id": str(self.id),
                "title": self.title,
                "url": self.url,
                "body": self.body,
                "user_id": self.user_id,
                }
    
    def save(self):
        Session.add(self)
        Session.commit()
