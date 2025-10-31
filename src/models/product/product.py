import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.models.cart.cart_item import CartItem
from src.models.order.order_item import OrderItem
from src.models.product.brand import Brand
from src.models.product.category import Category
from src.models.product.image import Image
from src.models.product.promotion import Promotion
from src.models.product.tag import Tag


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    name: str = Field(index=True, unique=True)
    summary: str
    description: str
    current_price: float = Field(..., alias="currentPrice")
    old_price: Optional[float] = Field(None, alias="oldPrice")
    rating: Optional[float] = None
    color: Optional[str] = None
    condition: Optional[str] = None
    badge_label: Optional[str] = Field(None, alias="badgeLabel")
    badge_color: Optional[str] = Field(None, alias="badgeColor")
    category_id: str = Field(foreign_key="categories.id", index=True)
    brand_id: str = Field(foreign_key="brands.id", index=True)
    stock: int = 0
    manufactured_at: Optional[datetime] = Field(None, alias="mfg")
    life_span_days: Optional[int] = Field(None, alias="life") 
    expiration_date: Optional[datetime] = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    category: Optional[Category] = Relationship(back_populates="products")
    brand: Optional[Brand] = Relationship(back_populates="products")
    promotions: List[Promotion] = Relationship(back_populates="products")
    images: List[Image] = Relationship(back_populates="product")
    tags: List[Tag] = Relationship(back_populates="products")
    cart_items: List["CartItem"] = Relationship(back_populates="product")
    order_items: List["OrderItem"] = Relationship(back_populates="product")
