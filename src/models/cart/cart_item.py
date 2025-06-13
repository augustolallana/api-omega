import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.cart.cart import Cart
    from src.models.product.product import Product


class CartItem(SQLModel, table=True):
    __tablename__ = "cart_items"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    cart_id: str = Field(foreign_key="carts.id", index=True)
    product_id: str = Field(foreign_key="products.id", index=True)
    quantity: int
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    cart: "Cart" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="cart_items")
