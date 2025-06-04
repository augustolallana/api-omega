from sqlmodel import Field, SQLModel

from src.models.base_response import BaseResponse


class User(SQLModel, table=True):
    """User model for the database."""

    id: str = Field(primary_key=True)
    password: str
    email: str = Field(unique=True, index=True)


class UserResponse(BaseResponse):
    user: User
