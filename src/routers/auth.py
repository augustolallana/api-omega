from fastapi import APIRouter
from starlette import status

from src.models.auth import (
    LoginCredentials,
    LoginResponse,
    LogoutResponse,
    RegisterCredentials,
    RegisterResponse,
)
from src.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(creds: LoginCredentials) -> LoginResponse:
    # Simulación de autenticación
    # Check creds
    # TODO add cookies or jwt

    return LoginResponse(
        message="Login successfully",
        status_code=status.HTTP_200_OK,
        bearer="example-token",
    )


# TODO check header parameters
@router.post("/logout", response_model=LogoutResponse)
async def logout() -> LogoutResponse:
    u = User(id=1, password="123", email="a@b.c")
    return LogoutResponse(
        message="User logged out.", status_code=status.HTTP_200_OK, user=u
    )


@router.post("/register", response_model=RegisterResponse)
async def register(user: RegisterCredentials) -> RegisterResponse:
    # Load user to db encrypting password
    # Simulación de registro
    return RegisterResponse(
        message="User created.", status_code=status.HTTP_201_CREATED, user=user
    )
