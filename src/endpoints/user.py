from typing import List
from uuid import UUID
from fastapi import APIRouter, status
from loguru import logger

from database.database import session_manager
from schemas.user import UserSchema
from services.crud.user import UserService


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create(user: UserSchema) -> UserSchema:
     logger.info("Starting create user")
     with session_manager() as session:
          service = UserService(session=session)
          user_created = service.create(user)
          return UserSchema.model_validate(user_created)
     
@router.get("/{user_uuid}", response_model=UserSchema, status_code=status.HTTP_200_OK)
def get(user_uuid: UUID):
     with session_manager() as session:
          service = UserService(session=session)
          user = service.get_by_id(user_uuid=user_uuid)
          return UserSchema.model_validate(user)

@router.get("/", response_model=List[UserSchema], status_code=status.HTTP_200_OK)
def get_all():
     with session_manager() as session:
          service = UserService(session=session)
          users = service.get_all()
          return [UserSchema.model_validate(user) for user in users]
