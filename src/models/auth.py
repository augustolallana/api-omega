from pydantic import BaseModel

from src.models.base_response import BaseResponse
from src.models.user import User


class LoginCredentials(BaseModel):
    email: str
    password: str

    # TODO add encryption. Check bcrypt.


class LoginResponse(BaseResponse):
    bearer: str


class RegisterResponse(BaseResponse):
    user: User
