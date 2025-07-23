from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from loguru import logger
from sqlalchemy.orm import Session

from database.database import get_db_session
from schemas.post import PostDBSchema, PostRequestSchema
from services.crud.post import PostService
from database.models.user import User
from services.auth import get_current_user


router = APIRouter(prefix="/post", tags=["Post"])


@router.post("/", response_model=PostDBSchema, status_code=status.HTTP_201_CREATED)
def create(
    post: PostRequestSchema,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> PostDBSchema:
    logger.info("Starting create post")
    service = PostService(session=session)
    post.user_id = current_user.id
    post_created = service.create(post)
    return PostDBSchema.model_validate(post_created)


@router.get("/{post_uuid}", response_model=PostDBSchema, status_code=status.HTTP_200_OK)
def get(
    post_uuid: UUID,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    service = PostService(session=session)
    post = service.get_by_id(post_uuid=post_uuid)
    return PostDBSchema.model_validate(post)


@router.get("/", response_model=List[PostDBSchema], status_code=status.HTTP_200_OK)
def get_all(
    session: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    service = PostService(session=session)
    posts = service.get_all()
    return [PostDBSchema.model_validate(post) for post in posts]
