from fastapi import APIRouter
from starlette import status

from src.models.user import User
from src.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user() -> UserResponse:
    # Simulate getting current user
    return UserResponse(
        message="User retrieved successfully.",
        status_code=status.HTTP_200_OK,
        user=None,
    )
