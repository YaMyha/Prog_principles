from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserR(BaseModel):
    id: Optional[int]
    username: str
    hashed_password: str
    email: str
    rating: Optional[int] = 0
    created_at: datetime


class UserC(BaseModel):
    username: str
    hashed_password: str
    email: str


class Post(BaseModel):
    author_id: int
    title: str
    description: str
    tags: str