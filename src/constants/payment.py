from enum import Enum


class PaymentMethodType(str, Enum):
    TRANSFER = "transfer"
    MERCADOPAGO = "mercadopago"
    CASH = "cash"
