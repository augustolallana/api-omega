from typing import Optional

from sqlmodel import Field, SQLModel

from src.constants.province import Province


class Address(SQLModel, table=True):
    __tablename__ = "addresses"

    id: str = Field(primary_key=True)
    province: Province
    city: str
    street: str
    number: int
    extra: Optional[str] = None
    postal_code: str
