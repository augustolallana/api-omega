from fastapi import APIRouter
from starlette import status

from src.schemas.base import BaseResponse

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=BaseResponse)
async def get_orders() -> BaseResponse:
    # Simular recuperación desde base de datos
    return BaseResponse(
        message="Orders retrieved successfully.",
        status_code=status.HTTP_200_OK,
        detail={"order": "order"},
    )
