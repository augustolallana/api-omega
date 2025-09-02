from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CartItemBase(BaseModel):
    """Base schema for cart items."""
    product_id: UUID = Field(..., description="ID of the product to add to cart")
    quantity: int = Field(..., ge=1, description="Quantity of the product")


class CartItemCreate(CartItemBase):
    """Schema for creating a new cart item."""
    pass


class CartItemUpdate(BaseModel):
    """Schema for updating a cart item."""
    quantity: int = Field(..., ge=1, description="New quantity of the product")


class CartItemResponse(CartItemBase):
    """Schema for cart item response."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Schema for cart response."""
    items: List[CartItemResponse]
    total_items: int
    total_price: float

    class Config:
        from_attributes = True
