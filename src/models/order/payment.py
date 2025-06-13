import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class PaymentMethodType(str, Enum):
    TRANSFER = "transfer"
    MERCADOPAGO = "mercadopago"


class PaymentMethod(SQLModel, table=True):
    __tablename__ = "payment_methods"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    type: PaymentMethodType
    details: str | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
