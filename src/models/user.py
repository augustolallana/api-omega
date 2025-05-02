from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    phone_number: str
