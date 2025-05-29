from pydantic import BaseModel

from src.models.base_response import BaseResponse


class User(BaseModel):
    id: str
    password: str
    email: str


class UserResponse(BaseResponse):
    user: User
