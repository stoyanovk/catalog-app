from db.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from models.user import User
from models.token import Token
from utils.password_utils import generate_password, check_password
from fastapi import Depends, HTTPException, status
from .validators import RegisterReqBodyValidator, LoginReqBodyValidator

from .user_service_response import UserData, TokenData


class UserService:
    def __init__(
        self,
        session: async_sessionmaker[AsyncSession] = Depends(get_session),
    ):
        self.session = session

    async def register(self, body: RegisterReqBodyValidator) -> UserData:
        bynary_pass = generate_password(body.password)

        async with self.session() as session:
            maybe_user = await User.get_user_by_email(session, body.email)
            if maybe_user:
                raise HTTPException(
                    status_code=422, detail="User with such email already exist"
                )
            user = await User.create_user(
                session, body.user_name, body.email, bynary_pass, body.phone
            )
        return UserData(
            id=user.id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            role=user.role,
        )

    async def login(self, body: LoginReqBodyValidator):
        async with self.session() as session:
            maybe_user = await User.get_user_by_email(session, body.email)
            if not maybe_user:
                raise HTTPException(
                    status_code=404, detail="User with this email is not exist"
                )
            is_pass_correct = check_password(body.password, maybe_user.password)
            if not is_pass_correct:
                raise HTTPException(status_code=403, detail="Wrong password")
            access_token = await Token.generate_token(session, maybe_user.id)
        return TokenData(
            access_token=access_token,
        )

    async def get_current_user(self, token: str) -> UserData:
        try:
            Token.check_token(token)
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token was expired",
                headers={"WWW-Authenticate": "Bearer"},  # не уверен в заголовках
            )

        async with self.session() as session:
            user = await User.get_user_by_token(session, token)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return UserData(
            id=user.id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            role=user.role.value,
        )

    async def logout(self, token: str):
        async with self.session() as session:
            try:
                await Token.remove(session, token)
                return {"message": "ok"}
            except:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something went wrong",
                )
