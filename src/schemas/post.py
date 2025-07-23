from datetime import date
from uuid import UUID

from pydantic import BaseModel


class PostDBSchema(BaseModel):
    title: str
    publication_date: date
    story: str
    user_id: UUID
    # images:

    class Config:
        from_attributes = True


class PostRequestSchema(BaseModel):
    title: str
    publication_date: date
    story: str
    user_id: UUID | None = None
    # images:

    class Config:
        from_attributes = True
