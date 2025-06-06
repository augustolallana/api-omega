from typing import List

from src.models.cart.cart import Cart
from src.models.cart.cart_item import CartItem
from src.schemas.base import BaseResponse


class CartResponse(BaseResponse):
    cart: Cart


class CartListResponse(BaseResponse):
    carts: List[Cart]


class CartItemResponse(BaseResponse):
    cart_item: CartItem


class CartItemListResponse(BaseResponse):
    cart_items: List[CartItem]
