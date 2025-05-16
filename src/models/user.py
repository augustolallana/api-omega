from pydantic import BaseModel


class User(BaseModel):
    id: str
    password: str
    email: str
