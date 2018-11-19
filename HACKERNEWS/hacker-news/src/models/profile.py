from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from database.base import Base, Session


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, ForeignKey("user.id"), primary_key=True, autoincrement=True)
    bio = Column(String)
    facebook_url = Column(String)

    def __repr__(self):
        return "<Profile id={}>".format(self.id)

    def __str__(self):
        return self.__repr__()

    def to_json(self):
        return {"id": str(self.id),
                "bio": self.bio,
                "facebook_url": self.facebook_url}
