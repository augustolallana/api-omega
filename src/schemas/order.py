from typing import List

from src.models.order.address import Address
from src.models.order.order import Order
from src.models.order.order_item import OrderItem
from src.models.order.payment_method import PaymentMethod
from src.schemas.base import BaseResponse


class OrderResponse(BaseResponse):
    order: Order


class OrderListResponse(BaseResponse):
    orders: List[Order]


class OrderItemResponse(BaseResponse):
    order_item: OrderItem


class OrderItemListResponse(BaseResponse):
    order_items: List[OrderItem]


class AddressResponse(BaseResponse):
    address: Address


class AddressListResponse(BaseResponse):
    addresses: List[Address]


class PaymentMethodResponse(BaseResponse):
    payment_method: PaymentMethod


class PaymentMethodListResponse(BaseResponse):
    payment_methods: List[PaymentMethod]
