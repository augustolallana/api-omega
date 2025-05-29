from enum import Enum

from pydantic import BaseModel

from src.models.base_response import BaseResponse
from src.models.cart import CartItem


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
    number: str
    postal_code: str
    extra: str | None = None  # documentar


class PaymentMethod(BaseModel):
    # TODO COMPLETAR
    type: str  # Maybe enum


class Order(BaseModel):
    id: str
    products: list[CartItem]
    first_name: str
    last_name: str
    phone_number: str
    address: Address
    payment_method: PaymentMethod


class OrderResponse(BaseResponse):
    order: Order
