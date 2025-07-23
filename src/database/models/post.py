from datetime import date
import uuid

from sqlalchemy import UUID, Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class Post(Base):
    __tablename__ = "post"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship(back_populates="post")  # noqa: F821

    title: Mapped[str] = mapped_column(String(30), nullable=False)
    story: Mapped[str] = mapped_column(Text, nullable=False)
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    ##TODO: add images

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, story={self.story}, date={self.date})"
