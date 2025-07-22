from datetime import date
import uuid

from sqlalchemy import UUID, Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import Base


class Post(Base):
    __tablename__ = "post"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    story: Mapped[str] = mapped_column(Text, nullable=False)
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    ##TODO: add images

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, story={self.story}, date={self.date})"
