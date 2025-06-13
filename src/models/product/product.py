import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.models.product.promotion import ProductPromotion
from src.models.product.tag import ProductTag

if TYPE_CHECKING:
    from src.models.cart.cart_item import CartItem
    from src.models.order.order_item import OrderItem
    from src.models.product.brand import Brand
    from src.models.product.category import Category
    from src.models.product.image import Image
    from src.models.product.promotion import Promotion
    from src.models.product.tag import Tag


class Product(SQLModel, table=True):
    """Product model for the database."""

    __tablename__ = "products"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    name: str = Field(index=True)
    summary: str
    description: str
    price: float
    category_id: str = Field(foreign_key="categories.id", index=True)
    brand_id: str = Field(foreign_key="brands.id", index=True)
    promotion_id: Optional[str] = Field(
        foreign_key="promotions.id", default=None, index=True
    )
    stock: int
    expiration_date: datetime
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    category: "Category" = Relationship(back_populates="products")
    brand: "Brand" = Relationship(back_populates="products")
    promotion: Optional["Promotion"] = Relationship(
        back_populates="products", link_model=ProductPromotion
    )
    images: List["Image"] = Relationship(back_populates="product")
    tags: List["Tag"] = Relationship(
        back_populates="products", link_model=ProductTag
    )
    cart_items: List["CartItem"] = Relationship(back_populates="product")
    order_items: List["OrderItem"] = Relationship(back_populates="product")
