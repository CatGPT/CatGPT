from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    created: datetime
    updated: datetime
    username: str
    firstName: str
    lastName: str
    email: str


class Register(BaseModel):
    username: str
    password: str
    firstName: str
    lastName: str
    email: str


class Token(BaseModel):
    username: str
    password: str


class Login(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class Refresh(BaseModel):
    access_token: str
    token_type: str


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "0lCU8ghbHhKCKFBw3UnVlQUyHSXOIKfZN2pdlUoDRkpY6TM6kleGveuIetQo9zS1"
    )
    authjwt_access_token_expires: timedelta = timedelta(hours=1)
    authjwt_refresh_token_expires: timedelta = timedelta(days=30)

class Image(BaseModel):
    id: int
    created: datetime
    updated: datetime
    imageURL: str
    share: bool

class SaveImage(BaseModel):
    imageURL: str
    share: bool

class Images(BaseModel):
    images: List[Image]

class Follow(BaseModel):
    id: int
    created: datetime
    updated: datetime
    followCnt: int
    followedBy: str

class SaveFollow(BaseModel):
    imageID: int