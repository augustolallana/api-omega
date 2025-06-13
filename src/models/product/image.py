import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.product.product import Product


class Image(SQLModel, table=True):
    __tablename__ = "images"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    url: str
    alt_text: str | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    product_id: str = Field(foreign_key="products.id")
    product: "Product" = Relationship(back_populates="images")
