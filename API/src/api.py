from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from auth.UserManager import get_user_manager
from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate
from db.modelsORM import User
from users_router import router as users_router
from posts_router import router as posts_router

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

app.include_router(users_router)
app.include_router(posts_router)
