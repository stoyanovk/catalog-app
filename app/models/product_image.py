from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column()
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
