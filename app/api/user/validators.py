from pydantic import BaseModel, Field, validator
from fastapi import HTTPException
import re


def email_validator(v):
    regExs = r"^.+@.+\..+$"
    if re.fullmatch(regExs, v):
        return v

    raise HTTPException(status_code=422, detail="Not match email")


class RegisterReqBodyValidator(BaseModel):
    user_name: str = Field(min_length=2, examples=["John"])
    email: str = Field(default=None, examples=["contact@gmail.com"])
    password: str = Field(min_length=4, examples=["1234"])
    phone: str = Field(default=None, examples=["+380999999999"])

    @validator("phone")
    def check_phone_number_format(cls, v):
        if v == "":
            return v
        regExs = r"^\+380\d{9}"
        if re.fullmatch(regExs, v):
            return v

        raise HTTPException(status_code=422, detail="Not match phone")

    @validator("email")
    def check_email(cls, v):
        return email_validator(v)


class LoginReqBodyValidator(BaseModel):
    email: str = Field(default=None, examples=["contact@gmail.com"])
    password: str = Field(min_length=4, examples=["1234"])

    @validator("email")
    def check_email(cls, v):
        return email_validator(v)
