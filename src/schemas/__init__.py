from src.schemas.admin import AdminResponse
from src.schemas.auth import (
    LoginCredentials,
    LoginResponse,
    LogoutResponse,
    RegisterCredentials,
    RegisterResponse,
    Token,
    TokenData,
)
from src.schemas.base import BaseResponse
from src.schemas.cart import (
    CartItemListResponse,
    CartItemResponse,
    CartListResponse,
    CartResponse,
)
from src.schemas.order import (
    AddressListResponse,
    AddressResponse,
    OrderItemListResponse,
    OrderItemResponse,
    OrderListResponse,
    OrderResponse,
    PaymentMethodListResponse,
    PaymentMethodResponse,
    Province,
)
from src.schemas.product import (
    BrandListResponse,
    BrandResponse,
    CategoryListResponse,
    CategoryResponse,
    ImageListResponse,
    ImageResponse,
    ProductListResponse,
    ProductResponse,
    PromotionListResponse,
    PromotionResponse,
    TagListResponse,
    TagResponse,
)
from src.schemas.user import UserResponse

__all__ = [
    # Base schemas
    "BaseResponse",
    # Auth schemas
    "Token",
    "TokenData",
    "LoginCredentials",
    "LoginResponse",
    "LogoutResponse",
    "RegisterCredentials",
    "RegisterResponse",
    # Admin schemas
    "AdminResponse",
    # User schemas
    "UserResponse",
    # Cart schemas
    "CartResponse",
    "CartListResponse",
    "CartItemResponse",
    "CartItemListResponse",
    # Order schemas
    "OrderResponse",
    "OrderListResponse",
    "OrderItemResponse",
    "OrderItemListResponse",
    "AddressResponse",
    "AddressListResponse",
    "PaymentMethodResponse",
    "PaymentMethodListResponse",
    "Province",
    # Product schemas
    "ProductResponse",
    "ProductListResponse",
    "CategoryResponse",
    "CategoryListResponse",
    "BrandResponse",
    "BrandListResponse",
    "TagResponse",
    "TagListResponse",
    "ImageResponse",
    "ImageListResponse",
    "PromotionResponse",
    "PromotionListResponse",
]
