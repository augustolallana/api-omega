from pydantic import BaseModel


class LoginCredentials(BaseModel):
    email: str
    password: str


class RegisterCredentials(BaseModel):
    email: str
    password: str
    username: str
