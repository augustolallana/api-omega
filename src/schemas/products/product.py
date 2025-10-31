from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    summary: str
    description: str
    current_price: float
    old_price: Optional[float] = None
    category_id: str
    brand_id: str
    stock: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    current_price: float
    old_price: Optional[float] = None
    category_id: Optional[str] = None
    brand_id: Optional[str] = None
    stock: Optional[int] = None
