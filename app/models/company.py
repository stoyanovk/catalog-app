from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
