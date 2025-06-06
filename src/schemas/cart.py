from typing import List

from src.schemas.base import BaseResponse


class CartResponse(BaseResponse):
    cart: str  # Cart


class CartListResponse(BaseResponse):
    carts: str  # List[Cart]


class CartItemResponse(BaseResponse):
    cart_item: str  # CartItem


class CartItemListResponse(BaseResponse):
    cart_items: str  # List[CartItem]
