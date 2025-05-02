from pydantic import BaseModel


class LoginCredentials(BaseModel):
    username: str
    password: str

    # TODO add encryption. Check bcrypt.
