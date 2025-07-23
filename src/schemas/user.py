import uuid
from pydantic import BaseModel
from datetime import date


class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class UserDBSchema(UserLoginSchema):
    id: uuid.UUID | None = None
    name: str
    born_date: date

    class Config:
        from_attributes = True
        # json_encoders = {uuid.UUID: str}


class UserResponseSchema(BaseModel):
    id: uuid.UUID | None = None
    name: str
    born_date: date
    email: str

    class Config:
        from_attributes = True
        # json_encoders = {uuid.UUID: str}


class UserCreateSchema(BaseModel):
    name: str
    born_date: date
    email: str
    password: str

    class Config:
        from_attributes = True
        # json_encoders = {uuid.UUID: str}
