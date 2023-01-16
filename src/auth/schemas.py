from pydantic import EmailStr
from datetime import datetime
from typing import Optional
from src.app.utils.schemas_utils import AbstractModel, ResponseModel


class TokenData(AbstractModel):
    email: EmailStr


class user_create(AbstractModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserResponse(AbstractModel):
    first_name: str
    last_name: str
    email: EmailStr
    date_created: datetime

    class Config:
        orm_mode = True


class UserUpdate(AbstractModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]


class MessageUserResponse(ResponseModel):
    data: UserResponse


class Token(AbstractModel):
    token: str


class AccessToken(Token):
    type: str


class RefreshToken(Token):
    header: str


class LoginResponse(AbstractModel):
    data: UserResponse
    access_token: AccessToken
    refresh_token: RefreshToken

    class Config:
        orm_mode = True


class MessageLoginResponse(ResponseModel):
    data: LoginResponse
