import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.product.product import Product


class ProductPromotion(SQLModel, table=True):
    """Link table for product-promotion many-to-many relationship."""

    product_id: str = Field(foreign_key="product.id", primary_key=True)
    promotion_id: str = Field(foreign_key="promotion.id", primary_key=True)


class Promotion(SQLModel, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    name: str
    description: str | None = None
    discount_percentage: float
    minimun_number_of_products: int
    start_date: datetime
    end_date: datetime
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    products: List["Product"] = Relationship(
        back_populates="promotions", link_model=ProductPromotion
    )
