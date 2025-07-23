from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from loguru import logger
from sqlalchemy.orm import Session

from database.database import get_db_session
from schemas.user import UserCreateSchema, UserResponseSchema
from services.crud.user import UserService
from database.models.user import User
from services.auth import get_current_user


router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED
)
def create(
    user: UserCreateSchema, session: Session = Depends(get_db_session)
) -> UserResponseSchema:
    logger.info("Starting create user")
    service = UserService(session=session)
    user_created = service.create(user)
    return UserResponseSchema.model_validate(user_created)


@router.get(
    "/{user_uuid}", response_model=UserResponseSchema, status_code=status.HTTP_200_OK
)
def get(
    user_uuid: UUID,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    service = UserService(session=session)
    user = service.get_by_id(user_uuid=user_uuid)
    return UserResponseSchema.model_validate(user)


##TODO: Add admin provileges
@router.get(
    "/", response_model=List[UserResponseSchema], status_code=status.HTTP_200_OK
)
def get_all(session: Session = Depends(get_db_session)):
    service = UserService(session=session)
    users = service.get_all()
    return [UserResponseSchema.model_validate(user) for user in users]
