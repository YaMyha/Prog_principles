from typing import List

from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from auth.UserManager import get_user_manager
from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate
from db.QueryManager import QueryManagerAsync
from db.database import get_async_session
from db.modelsORM import User
from validation_models import UserR, UserC

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
