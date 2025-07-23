import uuid
from pydantic import BaseModel
from datetime import date


class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class UserSchema(UserLoginSchema):
    id: uuid.UUID | None = None
    name: str
    born_date: date

    class Config:
        from_attributes = True
        json_encoders = {uuid.UUID: str}
