from typing import List

from fastapi import APIRouter

from container import post_service
from validation_models import PostC, PostR

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


@router.post("/")
async def add_post(post: PostC):
    post_id = await post_service.insert_post(**post.dict())
    return post_id


@router.get("/", response_model=List[PostR])
async def get_all_posts():
    return await post_service.select_posts()


# @router.get("/{author_name}", response_model=List[PostR])
# async def get_posts_by_author(author_name: str):
#     return await post_service.select_posts_by_author(author_name)


@router.get("/{tags}", response_model=List[PostR])
async def get_posts_by_tags(tags: str):
    return await post_service.select_posts_by_tags(tags)


@router.post("/update")
async def update_post(post: PostR):
    post_data = post.dict()
    post_id = post_data["id"]
    del post_data["id"]
    await post_service.update_post(post_id, post_data)
    return post_id


@router.delete("/{post_id}")
async def delete_post(post_id: int):
    await post_service.delete_post(post_id)
    return {"message": "Post deleted successfully"}