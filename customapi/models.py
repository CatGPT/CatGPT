from datetime import datetime

from customapi.database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from customapi.utils import get_password_hash


class Model(Base):
    __abstract__ = True
    __tablename__ = ""

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    created: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated: datetime = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class User(Model):
    __tablename__ = "user"

    username: str = Column(String(length=32), nullable=False, unique=True, index=True)
    password: str = Column(String(length=64), nullable=False)
    firstName: str = Column(String(length=255), nullable=False)
    lastName: str = Column(String(length=255), nullable=False)
    email: str = Column(String(length=64), nullable=False, unique=True)

    def __init__(self, password: str, **kwargs):
        super(User, self).__init__(**kwargs)
        self.generate_password_hash(password)

    def generate_password_hash(self, password: str) -> None:
        self.password = get_password_hash(password)

class Image(Model):
    __tablename__ = "image"

    userID: int = Column(Integer, nullable=False, index=True)
    imageURL: str = Column(String(length=2048), nullable=False, default="")
    share: bool = Column(Boolean, nullable=False, default=False)

class Follow(Model):
    __tablename__ = "follow"

    imageID: int = Column(Integer, nullable=False, index=True)
    followCnt: int = Column(Integer, nullable=False, unique=True, default=0)
    followedBy: str = Column(String(length=8192), nullable=False)