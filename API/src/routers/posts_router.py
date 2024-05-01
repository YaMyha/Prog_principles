import logging
from typing import List

from fastapi import APIRouter, HTTPException

from container import post_service
from validation_models import PostC, PostR

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


@router.post("/")
async def add_post(post: PostC):
    try:
        post_id = await post_service.insert_post(**post.dict())
        return {
            "status": "success",
            "post_id": post_id
        }
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "user_id": None,
            "details": "Server Error"
        })


@router.get("/")
async def get_posts(author_name: str = None, tags: str = None):
    try:
        parameters = {"author_name": author_name, "tags": tags}
        result = await post_service.select_posts(parameters)
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
async def update_post(post: PostR):
    try:
        post_data = post.dict()
        post_id = post_data["id"]
        del post_data["id"]
        await post_service.update_post(post_id, post_data)
        return {"status": "success"}
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "details": "Server Error"
        })


@router.delete("/{post_id}")
async def delete_post(post_id: int):
    try:
        await post_service.delete_post(post_id)
        return {"status": "success"}
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "details": "Server Error"
        })
