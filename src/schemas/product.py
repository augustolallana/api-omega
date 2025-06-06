from typing import List

from src.models.product.brand import Brand
from src.models.product.category import Category
from src.models.product.image import Image
from src.models.product.product import Product
from src.models.product.promotion import Promotion
from src.models.product.tag import Tag
from src.schemas.base import BaseResponse


class ProductResponse(BaseResponse):
    product: Product


class ProductListResponse(BaseResponse):
    products: List[Product]


class CategoryResponse(BaseResponse):
    category: Category


class CategoryListResponse(BaseResponse):
    categories: List[Category]


class BrandResponse(BaseResponse):
    brand: Brand


class BrandListResponse(BaseResponse):
    brands: List[Brand]


class TagResponse(BaseResponse):
    tag: Tag


class TagListResponse(BaseResponse):
    tags: List[Tag]


class ImageResponse(BaseResponse):
    image: Image


class ImageListResponse(BaseResponse):
    images: List[Image]


class PromotionResponse(BaseResponse):
    promotion: Promotion


class PromotionListResponse(BaseResponse):
    promotions: List[Promotion]
