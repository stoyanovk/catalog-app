from .base import Base
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import DateTime, ForeignKey, delete
from config.config import get_config
from sqlalchemy.ext.asyncio import AsyncSession

import jwt

CONFIG = get_config()


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column()
    created_at: Mapped[DateTime] = mapped_column(DateTime)

    @classmethod
    async def generate_token(cls, session: AsyncSession, user_id: int):
        access_token = jwt.encode(
            {
                "user_id": user_id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30),
            },
            CONFIG.ACCESS_JWT_SECRET,
            algorithm="HS256",
        )
        token = cls(token=access_token, user_id=user_id, created_at=datetime.now())
        session.add(token)
        await session.commit()
        return access_token

    @staticmethod
    def check_token(token: str):
        try:
            jwt.decode(token, CONFIG.ACCESS_JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError

    @classmethod
    async def remove(cls, session: AsyncSession, token: str):
        query = delete(cls).filter(cls.token == token)

        await session.execute(query)
        await session.commit()
