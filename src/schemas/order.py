from enum import Enum
from typing import List

from src.models.order.address import Address
from src.models.order.order import Order
from src.models.order.order_item import OrderItem
from src.models.order.payment_method import PaymentMethod
from src.schemas.base import BaseResponse


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
