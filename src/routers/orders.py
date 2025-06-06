from fastapi import APIRouter
from starlette import status

from src.schemas.order import OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=OrderResponse)
async def get_orders() -> OrderResponse:
    # Simular recuperación desde base de datos
    return OrderResponse(
        message="Orders retrieved successfully.",
        status_code=status.HTTP_200_OK,
        order=None,
    )
