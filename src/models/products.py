from datetime import datetime
from enum import Enum

from pydantic import BaseModel


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
