import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

from src.models.order.address import Address
from src.models.order.order_item import OrderItem
from src.models.order.payment import PaymentMethod

if TYPE_CHECKING:
    from src.models.user import User


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    user_id: str = Field(foreign_key="users.id", index=True)
    address_id: str = Field(foreign_key="addresses.id", index=True)
    payment_method_id: str = Field(
        foreign_key="payment_methods.id", index=True
    )
    total_amount: float
    status: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    user: "User" = Relationship(back_populates="orders")
    address: Address = Relationship()
    payment_method: PaymentMethod = Relationship()
    items: List["OrderItem"] = Relationship(back_populates="order")
