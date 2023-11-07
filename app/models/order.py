import enum
from .base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Enum, DateTime


class Statuses(enum.Enum):
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column()
    client_id: Mapped[
        str
    ] = (
        mapped_column()
    )  # пользователь может быть не зарегестрирован, но у него должен быть уникальный идентификатор
    created_at: Mapped[DateTime] = mapped_column(DateTime)
    total_amount: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(Enum(Statuses), default=Statuses.processing)
