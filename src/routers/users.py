from fastapi import APIRouter
from starlette import status

from src.schemas.base import BaseResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=BaseResponse)
async def get_current_user() -> BaseResponse:
    # Simulate getting current user
    return BaseResponse(
        message="User retrieved successfully.",
        status_code=status.HTTP_200_OK,
        detail={"user": "user"},
    )
