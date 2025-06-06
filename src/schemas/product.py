from typing import List

from src.schemas.base import BaseResponse


class ProductResponse(BaseResponse):
    product: str  # Product


class ProductListResponse(BaseResponse):
    products: str  # List[Product]


class CategoryResponse(BaseResponse):
    category: str  # Category


class CategoryListResponse(BaseResponse):
    categories: str  # List[Category]


class BrandResponse(BaseResponse):
    brand: str  # Brand


class BrandListResponse(BaseResponse):
    brands: str  # List[Brand]


class TagResponse(BaseResponse):
    tag: str  # Tag


class TagListResponse(BaseResponse):
    tags: str  # List[Tag]


class ImageResponse(BaseResponse):
    image: str  # Image


class ImageListResponse(BaseResponse):
    images: str  # List[Image]


class PromotionResponse(BaseResponse):
    promotion: str  # Promotion


class PromotionListResponse(BaseResponse):
    promotions: str  # List[Promotion]
