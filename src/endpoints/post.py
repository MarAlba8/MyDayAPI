from typing import List
from uuid import UUID
from fastapi import APIRouter, status
from loguru import logger

from database.database import session_manager
from schemas.post import PostSchema
from services.crud.post import PostService


router = APIRouter(prefix="/post", tags=["Post"])


@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
def create(post: PostSchema) -> PostSchema:
    logger.info("Starting create post")
    with session_manager() as session:
        service = PostService(session=session)
        post_created = service.create(post)
        return PostSchema.model_validate(post_created)


@router.get("/{post_uuid}", response_model=PostSchema, status_code=status.HTTP_200_OK)
def get(post_uuid: UUID):
    with session_manager() as session:
        service = PostService(session=session)
        post = service.get_by_id(post_uuid=post_uuid)
        return PostSchema.model_validate(post)


@router.get("/", response_model=List[PostSchema], status_code=status.HTTP_200_OK)
def get_all():
    with session_manager() as session:
        service = PostService(session=session)
        posts = service.get_all()
        return [PostSchema.model_validate(post) for post in posts]
