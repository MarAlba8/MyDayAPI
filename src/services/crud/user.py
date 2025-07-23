from uuid import UUID
from loguru import logger
from psycopg2.errors import UniqueViolation
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError

from database.models.user import User
from services.auth import UserManager
from schemas.user import UserCreateSchema
from core.exceptions import ExistingEmailError


class UserService:
    def __init__(self, session):
        self.session = session

    def create(self, user: UserCreateSchema):
        logger.info("Creating user")

        user_manager = UserManager()
        hashed_password = user_manager.hash_password(password=user.password)
        user.password = hashed_password

        user = User(**user.model_dump())

        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise ExistingEmailError(
                    "The email is already occupied by another account"
                )
        except Exception as e:
            raise e
        return user

    def get_by_id(self, user_uuid: UUID):
        logger.info("Getting user")
        query = select(User).where(User.id == user_uuid)
        user = self.session.execute(query).scalars().first()

        if not user:
            raise NoResultFound(f"Not user found with id: {(user_uuid)}")

        return user

    def get_all(self):
        query = select(User)
        return self.session.execute(query).scalars().all()
