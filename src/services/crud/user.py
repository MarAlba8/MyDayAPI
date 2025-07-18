from uuid import UUID
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.models.user import User

class UserService:
     def __init__(self, session):
          self.session = session

     def create(self, user):
          logger.info("Creating user")
          user = User(**user.model_dump())
          self.session.add(user)
          self.session.commit()
          self.session.refresh(user)
          return user
     
     def get_by_id(self, user_uuid: UUID):
          logger.info("Getting user")
          query = select(User).where(User.id==user_uuid)
          user = self.session.execute(query).scalars().first()

          if not user:
               raise NoResultFound(f"Not user found with id: {(user_uuid)}")
          
          return user
     
     def get_all(self):
          query = select(User)
          return self.session.execute(query).scalars().all()
          