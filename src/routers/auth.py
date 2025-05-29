from fastapi import APIRouter
from starlette import status

from src.models.auth import LoginCredentials, LoginResponse, RegisterResponse
from src.models.base_response import BaseResponse
from src.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
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
@router.post("/logout")
async def logout() -> BaseResponse:
    return BaseResponse(
        message="User logged out", status_code=status.HTTP_200_OK
    )


@router.post("/register")
async def register(user: User) -> RegisterResponse:
    # Load user to db encrypting password
    # Simulación de registro
    return RegisterResponse(
        message="User created.", status_code=status.HTTP_201_CREATED, user=user
    )
