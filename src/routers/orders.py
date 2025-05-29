from fastapi import APIRouter
from starlette import status

from src.models.order import (
    Address,
    Order,
    OrderResponse,
    PaymentMethod,
    Province,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=OrderResponse)
async def get_orders() -> OrderResponse:
    # Simular recuperación desde base de datos
    o = Order(
        id="order001",
        products=[],
        first_name="Juan",
        last_name="Pérez",
        phone_number="1134567890",
        address=Address(
            province=Province.CORDOBA,
            city="Córdoba",
            street="Av. Colón",
            number="1234",
            postal_code="5000",
        ),
        payment_method=PaymentMethod(type="platita"),
    )
    return OrderResponse(
        message="Orders retrieved successfully.",
        status_code=status.HTTP_200_OK,
        order=o,
    )
