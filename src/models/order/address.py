import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.order.order import Order
    from src.models.user import User


class Province(str, Enum):
    """Province enum for Argentina."""

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


class Address(SQLModel, table=True):
    """Address model for the database."""

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    user_id: str = Field(foreign_key="user.id", index=True)
    country: str = Field(default="Argentina")
    state: Province
    city: str
    street: str
    number: int
    extra: str
    postal_code: str
    is_default: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    user: "User" = Relationship(back_populates="addresses")
    orders: List["Order"] = Relationship(back_populates="address")
