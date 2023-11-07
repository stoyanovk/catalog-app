from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from .user_service import UserService
from .validators import RegisterReqBodyValidator, LoginReqBodyValidator
from .user_service_response import UserData, TokenData

user_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@user_router.post(
    "/register",
    response_model=UserData,
)
async def create(
    data: RegisterReqBodyValidator,
    use_case: UserService = Depends(UserService),
):
    return await use_case.register(data)


@user_router.post(
    "/login",
    response_model=TokenData,
)
async def login(
    data: LoginReqBodyValidator,
    use_case: UserService = Depends(UserService),
):
    return await use_case.login(data)


@user_router.delete(
    "/login",
)
async def logout(
    use_case: UserService = Depends(UserService),
    HTTPBearer: str = Header(
        default=None,
        example="JWT token",
    ),
):
    return await use_case.logout(HTTPBearer)


@user_router.get("/users/me", response_model=UserData)
async def get_user(
    use_case: UserService = Depends(UserService),
    HTTPBearer: str = Header(
        default=None,
        example="JWT token",
    ),
):
    return await use_case.get_current_user(HTTPBearer)
