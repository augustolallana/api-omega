import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

from src.models.order.address import Address
from src.models.order.order_item import OrderItem

if TYPE_CHECKING:
    from src.models.order.payment_method import PaymentMethod
    from src.models.user import User


class Order(SQLModel, table=True):
    """Order model for the database."""

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    user_id: str = Field(foreign_key="user.id", index=True)
    address_id: str = Field(foreign_key="address.id", index=True)
    payment_method_id: str = Field(foreign_key="paymentmethod.id", index=True)
    total_amount: float
    status: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    user: "User" = Relationship(back_populates="orders")
    address: Address = Relationship(back_populates="orders")
    payment_method: "PaymentMethod" = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")
