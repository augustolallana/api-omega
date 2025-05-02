from fastapi import APIRouter, Cookie

from src.models.auth import LoginCredentials
from src.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def login(creds: LoginCredentials) -> Cookie:
    # Check creds
    # TODO add cookies or jwt
    return {"message": "Login successfully", "bearer": "bearer"}


# TODO check header parameters
@router.get("/logout")
async def logout():
    pass


@router.get("/register")
async def register(user: User):
    # Load user to db encrypting password
    return {"message": "User created", "user": user.model_dump()}
