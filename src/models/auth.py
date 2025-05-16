from pydantic import BaseModel


class LoginCredentials(BaseModel):
    email: str
    password: str

    # TODO add encryption. Check bcrypt.
