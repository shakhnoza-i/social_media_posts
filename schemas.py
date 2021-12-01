from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, time


class User(BaseModel):
    username: str
    
    class Config():
        orm_mode = True


class Comment(BaseModel):
    username: str
    text: str
    timestamp: datetime

    class Config():
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str
    password: str


class PostBase(BaseModel):
    image_url: str # absolute path
    image_url_type: str # relative path
    caption: str
    creator_id: int


class CommentBase(BaseModel):
    username: str
    text: str
    post_id: int


class UserDisplay(BaseModel):
    username: str
    email: str

    class Config(): # allows us to convert our modeltype to this schema type
        orm_mode = True # convert orm to json


class PostDisplay(BaseModel):
    id: int
    image_url: str # absolute path
    image_url_type: str # relative path
    caption: str
    timestamp: datetime
    user: User
    comments: List[Comment]

    class Config():
        orm_mode = True

