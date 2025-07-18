from datetime import date
import uuid
from sqlalchemy import UUID, Date, String
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import Base


class User(Base):
     __tablename__ = "user"

     id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
     name: Mapped[str] = mapped_column(String(30), nullable=False)
     email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True) ##TODO: add unique constraint in DB
     password: Mapped[str] = mapped_column(String(30), nullable=False)
     born_date: Mapped[date] = mapped_column(Date, nullable=True)

     def __repr__(self):
          return f"User(id={self.id}, name={self.name}, email={self.emai})"
     