from typing import Optional

from pydantic import BaseModel

from src.models.user import User
from src.schemas.base import BaseResponse


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginCredentials(BaseModel):
    email: str
    password: str


class LoginResponse(BaseResponse):
    bearer: str


class LogoutResponse(BaseResponse):
    user: User


class RegisterCredentials(BaseModel):
    email: str
    password: str
    username: str


class RegisterResponse(BaseResponse):
    user: RegisterCredentials
