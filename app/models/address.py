from .base import Base
from sqlalchemy.orm import mapped_column, Mapped


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column()
    client_id: Mapped[str] = mapped_column()
    street_address: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
