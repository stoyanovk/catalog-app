from pydantic import BaseModel


class UserData(BaseModel):
    id: int
    name: str
    email: str
    role: str
    phone: str | None = None


class TokenData(BaseModel):
    access_token: str
