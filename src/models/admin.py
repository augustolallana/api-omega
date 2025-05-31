from src.models.base_response import BaseResponse
from src.models.user import User


class Admin(User):
    is_admin: bool = True


class AdminResponse(BaseResponse):
    is_admin: bool
