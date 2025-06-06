from enum import Enum
from typing import List

from pydantic import BaseModel

from src.models.order.order import Order
from src.models.order.order_item import OrderItem
from src.schemas.base import BaseResponse


class PaymentMethod(str, Enum):
    TRANSFER = "transfer"
    MERCADOPAGO = "mercadopago"


class Province(str, Enum):
    BUENOS_AIRES = "Buenos Aires"
    CABA = "Ciudad Autónoma de Buenos Aires"
    CATAMARCA = "Catamarca"
    CHACO = "Chaco"
    CHUBUT = "Chubut"
    CORDOBA = "Córdoba"
    CORRIENTES = "Corrientes"
    ENTRE_RIOS = "Entre Ríos"
    FORMOSA = "Formosa"
    JUJUY = "Jujuy"
    LA_PAMPA = "La Pampa"
    LA_RIOJA = "La Rioja"
    MENDOZA = "Mendoza"
    MISIONES = "Misiones"
    NEUQUEN = "Neuquén"
    RIO_NEGRO = "Río Negro"
    SALTA = "Salta"
    SAN_JUAN = "San Juan"
    SAN_LUIS = "San Luis"
    SANTA_CRUZ = "Santa Cruz"
    SANTA_FE = "Santa Fe"
    SANTIAGO_DEL_ESTERO = "Santiago del Estero"
    TIERRA_DEL_FUEGO = "Tierra del Fuego"
    TUCUMAN = "Tucumán"


class Address(BaseModel):
    province: Province
    city: str
    street: str
    number: int
    extra: str
    postal_code: str


class OrderResponse(BaseResponse):
    order: Order


class OrderListResponse(BaseResponse):
    orders: List[Order]


class OrderItemResponse(BaseResponse):
    order_item: OrderItem


class OrderItemListResponse(BaseResponse):
    order_items: List[OrderItem]
