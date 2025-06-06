from src.models.user import User
from src.schemas.base import BaseResponse


class UserResponse(BaseResponse):
    user: User
