from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import select, join
from sqlalchemy import Enum, LargeBinary
from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base
from .token import Token
from typing import Self
import enum


class Roles(enum.Enum):
    admin = "admin"
    moderator = "moderator"
    customer = "customer"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[bytes] = mapped_column(LargeBinary())
    role: Mapped[str] = mapped_column(Enum(Roles), default=Roles.customer.value)
    phone: Mapped[str | None] = mapped_column(default=None)

    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, id: int):
        query = select(cls).filter(cls.id == id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, email: str) -> Self | None:
        query = select(cls).filter(cls.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_user_by_token(cls, session: AsyncSession, token: str) -> Self | None:
        query = select(cls).join(Token).filter(Token.token == token)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def create_user(
        cls,
        session: AsyncSession,
        name: str,
        email: str,
        password: bytes,
        phone: str | None,
    ):
        user = User(name=name, email=email, password=password, phone=phone)
        session.add(user)
        await session.commit()

        new_user = await cls.get_user_by_id(session, user.id)
        if not new_user:
            raise RuntimeError()
        return new_user
