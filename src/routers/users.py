from fastapi import APIRouter

from src.models import User
from src.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user() -> UserResponse:
    # Retrieve from db
    u = User(id=1, email="a@b.c", password="123")
    return UserResponse(message="me", status_code=200, user=u)
