import logging
from typing import List
from fastapi import APIRouter, HTTPException

from container import user_service
from validation_models import UserR, UserC, UserU

router = APIRouter(
    prefix="/users",
    tags=["User"]
)


@router.post("/")
async def add_user(user: UserC):
    try:
        user_id = await user_service.insert_user(**user.dict())
        return {
            "status": "success",
            "user_id": user_id
        }
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "user_id": None,
            "details": "Server Error"
        })


@router.get("/")
async def get_users(user_id: int = None, rating_bottom: int = None, rating_top: int = None):
    try:
        parameters = {"user_id": user_id, "rating_bottom": rating_bottom, "rating_top": rating_top}
        result = await user_service.select_posts(parameters)
        return {
            "status": "success",
            "data": result,
            "details": None
        }
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Server Error"
        })


@router.put("/update")
async def update_user(user: UserU):
    try:
        user_data = user.dict()
        user_id = user_data["id"]
        del user_data["id"]
        await user_service.update_user(user_id, user_data)
        return {"status": "success"}
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "details": "Server Error"
        })


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    try:
        await user_service.delete_user(user_id)
        return {"status": "success"}
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "details": "Server Error"
        })
