import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

from src.models.cart.cart_item import CartItem

if TYPE_CHECKING:
    from src.models.user import User


class Cart(SQLModel, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    user: "User" = Relationship(back_populates="cart")
    items: List["CartItem"] = Relationship(back_populates="cart")
