from fastapi import APIRouter
from starlette import status

from src.schemas.admin import AdminResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login", response_model=AdminResponse)
async def admin_login() -> AdminResponse:
    # Simulate admin login
    return AdminResponse(
        message="Admin login successful.",
        status_code=status.HTTP_200_OK,
        admin=None,
    )
