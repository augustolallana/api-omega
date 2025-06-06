from typing import Optional

from pydantic import BaseModel

from src.models.user import User
from src.schemas.base import BaseResponse


class Token(BaseModel):
    """Token model for authentication."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model for authentication."""

    email: Optional[str] = None


class LoginCredentials(BaseModel):
    """Login credentials model."""

    email: str
    password: str


class LoginResponse(BaseResponse):
    """Login response model."""

    bearer: str


class LogoutResponse(BaseResponse):
    """Logout response model."""

    user: User


class RegisterCredentials(BaseModel):
    """Register credentials model."""

    email: str
    password: str
    username: str


class RegisterResponse(BaseResponse):
    """Register response model."""

    user: RegisterCredentials
