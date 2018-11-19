import datetime
import hashlib
import logging
import re

import bcrypt
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import relationship

from database.base import Base, Session
from models.profile import Profile

GAVATAR_HOST = "https://www.gravatar.com/avatar/"
DEFAULT_AVATAR = GAVATAR_HOST + "00000000000000000000000000000000"
EMAIL_PATTERN = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


class User(Base):
    __tablename__ = "user"
    # Attributes:
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    _password = Column(String, nullable=False)
    _email = Column(String)
    _avatar = Column(String)
    # Relation:
    profile = relationship("Profile", uselist=False)
    created_at = Column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )

    @hybrid_property
    def password(self):
        return self._password

    @password.setter  # type: ignore
    def password(self, plain_password):
        self._password = bcrypt.hashpw(
            plain_password.encode(), bcrypt.gensalt()
        ).decode()
    
    @hybrid_property
    def email(self):
        return self._email

    
    @email.setter  # type: ignore
    def email(self, email: str):
        pattern = re.compile(EMAIL_PATTERN)
        if pattern.match(email):
            self._email = email
        else:
            raise ValueError("Email is not valid format.")

    @hybrid_property
    def avatar(self):
        if self._avatar:
            return self._avatar
        elif self.email:
            email_hash = hashlib.md5(self.email.encode()).hexdigest()
            return GAVATAR_HOST + email_hash
        else:
            return DEFAULT_AVATAR

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User id={} username={} email={}>".format(
            self.id, self.username, self.email
        )

    def __str__(self):
        return self.__repr__()

    @classmethod
    def get_all(cls):
        return Session.query(cls).all()

    @classmethod
    def authorization(cls, username: str, password: str):
        account = Session.query(cls).filter(User.username == username).first()
        if not account:
            logging.debug("Account not found")
            return None
        if not bcrypt.checkpw(password.encode(), account.password.encode()):
            logging.debug("Account password mismatch")
            return None
        return account

    def save(self):
        Session.add(self)
        Session.commit()

    def to_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "avatar": self.avatar,
            "profile": self.profile.to_json() if self.profile else {},
        }
