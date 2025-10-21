from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from src.constants.payment import PaymentMethodType
from src.constants.province import Province


# ADDRESS SCHEMAS
class AddressBase(BaseModel):
    province: Province
    city: str
    street: str
    number: int
    extra: Optional[str] = None
    postal_code: str


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: str

    class Config:
        from_attributes = True


# PAYMENT METHOD SCHEMAS
class PaymentMethodBase(BaseModel):
    type: PaymentMethodType
    details: Optional[str] = None


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodResponse(PaymentMethodBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ORDER ITEM SCHEMAS
class OrderItemBase(BaseModel):
    product_id: str
    quantity: int


class OrderItemCreate(OrderItemBase):
    unit_price: float


class OrderItemResponse(OrderItemBase):
    id: str
    order_id: str

    class Config:
        from_attributes = True


# ORDER SCHEMAS
class OrderBase(BaseModel):
    user_id: str
    address_id: str
    payment_method_id: str
    total_amount: float


class OrderCreate(OrderBase):
    items: List[OrderItemBase]


class OrderUpdate(BaseModel):
    address_id: Optional[str] = None
    payment_method_id: Optional[str] = None
    status: Optional[str] = None
    total_amount: Optional[float] = None


class OrderResponse(OrderBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse]
    address: AddressResponse
    payment_method: PaymentMethodType

    class Config:
        from_attributes = True
