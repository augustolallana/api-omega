from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from src.models.base_response import BaseResponse


class Image(BaseModel):
    id: str
    description: str
    url: str


class Category(BaseModel):
    id: str
    name: str


class Brand(BaseModel):
    id: str
    name: str


class Tag(BaseModel):
    id: str
    name: str


class Promotion(Enum):
    pass


class Offer(BaseModel):
    id: str
    promotion: Promotion
    discount: float


class Product(BaseModel):
    id: str
    name: str
    summary: str
    description: str
    price: float
    images: list[Image]
    category: Category
    rating: int
    brand: Brand
    tags: list[Tag] | None = None
    stock: int
    expiration_date: datetime
    offer: Offer


class ProductsResponse(BaseResponse):
    products: Optional[list[Product]]
    old_product: Optional[Product]
    new_product: Optional[Product]
