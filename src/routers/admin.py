from fastapi import APIRouter
from starlette import status

from src.schemas import AdminResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/", response_model=AdminResponse)
async def admin():
    return AdminResponse(
        message="Admin login.",
        status_code=status.HTTP_202_ACCEPTED,
        is_admin=True,
    )
