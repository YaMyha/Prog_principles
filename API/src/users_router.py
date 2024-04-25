from typing import List
from fastapi import APIRouter

from container import user_service
from validation_models import UserR, UserC, UserU

router = APIRouter(
    prefix="/users",
    tags=["User"]
)


@router.get("/", response_model=List[UserR])
async def get_all_users():
    return await user_service.select_users()


@router.get("/top", response_model=List[UserR])
async def get_top_users():
    return await user_service.select_users_with_positive_rating_and_filled_email()


@router.post("/")
async def add_user(user: UserC):
    user_id = await user_service.insert_user(**user.dict())
    return user_id


@router.post("/update")
async def update_user(user: UserU):
    user_data = user.dict()
    user_id = user_data["id"]
    del user_data["id"]
    await user_service.update_user(user_id, user_data)
    return user_id


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    await user_service.delete_user(user_id)
    return {"message": "User deleted successfully"}
