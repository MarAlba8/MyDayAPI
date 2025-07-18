from typing import List, Optional
import uuid
from pydantic import BaseModel
from datetime import date


class UserSchema(BaseModel):
     id: Optional[uuid.UUID] = None
     name: str
     email: str
     password: str
     born_date: date

     class Config:
          from_attributes = True
          # orm_mode = True


# class UserListSchema(BaseModel):
#      users: List[UserSchema]

#      class Config:
#           from_attributes = True

