from fastapi import APIRouter

from src.models.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_current_user() -> UserResponse:
    return UserResponse(message="me", status_code=200)
