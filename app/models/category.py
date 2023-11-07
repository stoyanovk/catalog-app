from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from .base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    alias: Mapped[str] = mapped_column()
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
