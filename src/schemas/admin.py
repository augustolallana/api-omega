from src.models.user import User
from src.schemas.base import BaseResponse


class AdminResponse(BaseResponse):
    """Admin response model."""

    admin: User
