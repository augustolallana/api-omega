from pydantic import BaseModel

from src.models.base_response import BaseResponse


class LoginCredentials(BaseModel):
    email: str
    password: str

    # TODO add encryption. Check bcrypt.


class LoginResponse(BaseResponse):
    bearer: str
