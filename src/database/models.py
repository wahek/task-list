from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Text, DateTime

from src.main.schemas import TagEnum
from datetime import datetime

Base = declarative_base()
metadata = Base.metadata


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text())
    deadline: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True, default=None)
    tags: Mapped[TagEnum | None] = mapped_column(String(50), default=None)
    completed: Mapped[bool] = mapped_column(Boolean(), default=False)
    date_created: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now().replace(microsecond=0))
