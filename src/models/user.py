from enum import Enum

from pydantic import BaseModel


class Province(Enum):
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
    numero: str
    extra: str | None = None


class User(BaseModel):
    id: str
    first_name: str
    last_name: str
    username: str
    password: str
    phone_number: str
    email: str
    address: Address
