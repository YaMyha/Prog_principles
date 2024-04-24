from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from pydantic import BaseModel

from QueryManager import QueryManagerAsync
from auth.UserManager import get_user_manager
from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate
from modelsORM import User


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


query_manager = QueryManagerAsync()

app = FastAPI(title="Hobby Trading", debug=True)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/users", response_model=List[UserR])
async def get_user():
    return await query_manager.select_users()


@app.get("/users/top", response_model=List[UserR])
async def get_user():
    return await query_manager.select_users_with_positive_rating_and_filled_email()


@app.post("/users")
async def add_user(user: UserC):
    user_id = await query_manager.insert_user(**user.dict())
    return user_id
