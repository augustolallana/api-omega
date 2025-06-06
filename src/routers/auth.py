from fastapi import APIRouter
from starlette import status

from src.models.user import User
from src.schemas.auth import (
    LoginCredentials,
    LoginResponse,
    LogoutResponse,
    RegisterCredentials,
    RegisterResponse,
)
from src.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginCredentials) -> LoginResponse:
    # Simulate login
    return LoginResponse(
        message="Login successful.",
        status_code=status.HTTP_200_OK,
        bearer="dummy_token",
    )


@router.post("/logout", response_model=LogoutResponse)
async def logout() -> LogoutResponse:
    # Simulate logout
    return LogoutResponse(
        message="Logout successful.", status_code=status.HTTP_200_OK, user=None
    )


@router.post("/register", response_model=RegisterResponse)
async def register(credentials: RegisterCredentials) -> RegisterResponse:
    # Simulate registration
    return RegisterResponse(
        message="Registration successful.",
        status_code=status.HTTP_201_CREATED,
        user=credentials,
    )
