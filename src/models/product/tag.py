import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.product.product import Product


class ProductTag(SQLModel, table=True):
    __tablename__ = "product_tags"

    product_id: str = Field(foreign_key="products.id", primary_key=True)
    tag_id: str = Field(foreign_key="tags.id", primary_key=True)


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    name: str = Field(index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    products: List["Product"] = Relationship(
        back_populates="tags", link_model=ProductTag
    )
