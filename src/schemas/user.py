from typing import Optional
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
