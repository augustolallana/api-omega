from pydantic import BaseModel

from src.models.base_response import BaseResponse
from src.models.user import User


class RegisterCredentials(BaseModel):
    email: str
    password: str


class LoginCredentials(BaseModel):
    email: str
    password: str

    # TODO add encryption. Check bcrypt.


class RegisterResponse(BaseResponse):
    user: User


class LoginResponse(BaseResponse):
    bearer: str


class LogoutResponse(BaseResponse):
    user: User
