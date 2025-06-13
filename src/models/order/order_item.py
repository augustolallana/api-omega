import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.order.order import Order
    from src.models.product.product import Product


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    order_id: str = Field(foreign_key="orders.id", index=True)
    product_id: str = Field(foreign_key="products.id", index=True)
    quantity: int
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    order: "Order" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="order_items")
