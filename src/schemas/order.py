from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from src.models.order.address import Province
from src.models.order.payment import PaymentMethodType


class PaymentMethod(str, Enum):
    TRANSFER = "transfer"
    MERCADOPAGO = "mercadopago"


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


class OrderItemBase(BaseModel):
    product_id: str
    quantity: int
    unit_price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: str
    order_id: str

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    user_id: str
    address_id: str
    payment_method_id: str
    total_amount: float


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


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
    payment_method: PaymentMethodResponse

    class Config:
        from_attributes = True
