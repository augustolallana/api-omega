from fastapi import APIRouter
from starlette import status

from src.schemas.auth import (
    LoginCredentials,
    RegisterCredentials,
)
from src.schemas.base import BaseResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=BaseResponse)
async def login(credentials: LoginCredentials) -> BaseResponse:
    # Simulate login
    return BaseResponse(
        message="Login successful.",
        status_code=status.HTTP_200_OK,
        detail={"credentials": credentials, "bearer": "dummy_token"},
    )


@router.post("/logout", response_model=BaseResponse)
async def logout() -> BaseResponse:
    # Simulate logout
    return BaseResponse(
        message="Logout successful.",
        status_code=status.HTTP_200_OK,
        detail={"user.is_active": False},
    )


@router.post("/register", response_model=BaseResponse)
async def register(credentials: RegisterCredentials) -> BaseResponse:
    # Simulate registration
    return BaseResponse(
        message="Registration successful.",
        status_code=status.HTTP_201_CREATED,
        detail={"user.id": "user.id", "credentials": credentials},
    )
