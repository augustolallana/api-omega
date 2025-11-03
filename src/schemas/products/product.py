from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    current_price: float
    old_price: Optional[float] = None
    rating: float
    brand_id: str
    category_id: str
    color: str
    condition: str
    description: str
    stock: int
    life: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    current_price: Optional[float] = None
    old_price: Optional[float] = None
    rating: Optional[float] = None
    brand_id: Optional[str] = None
    category_id: Optional[str] = None
    color: Optional[str] = None
    condition: Optional[str] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    life: Optional[str] = None
