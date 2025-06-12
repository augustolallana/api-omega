import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

from src.models.order.order_item import OrderItem

if TYPE_CHECKING:
    from src.models.user import User

from src.schemas.order import Address, PaymentMethod


class Order(SQLModel, table=True):
    """Order model for the database."""

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    user_id: str = Field(foreign_key="user.id", index=True)
    address: Address
    payment_method: PaymentMethod
    total_amount: float
    status: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    user: "User" = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")
