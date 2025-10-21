import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.cart.cart import Cart
    from src.models.order.order import Order


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(unique=True, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str = Field(index=True)
    last_name: str = Field(index=True)
    username: str = Field(
        unique=True, index=True
    )  # recortar a 12 caracteres concatenando nombre y apellido
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    cart: "Cart" = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")
