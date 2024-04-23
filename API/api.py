from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from QueryManager import QueryManagerAsync

app = FastAPI(title="Hobby Trading", debug=True)


class UserRead(BaseModel):
    id: Optional[int]
    username: str
    password_hash: str
    email: str
    rating: Optional[int] = 0
    created_at: datetime


class UserCreate(BaseModel):
    username: str
    password_hash: str
    email: str


class Post(BaseModel):
    author_id: int
    title: str
    description: str
    tags: str


query_manager = QueryManagerAsync()


@app.get("/users", response_model=List[UserRead])
async def get_user():
    return await query_manager.select_users()


@app.get("/users/top", response_model=List[UserRead])
async def get_user():
    return await query_manager.select_users_with_positive_rating_and_filled_email()


@app.post("/users")
async def add_user(user: UserCreate):
    user_id = await query_manager.insert_user(**user.dict())
    return user_id
