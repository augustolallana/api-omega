from fastapi import APIRouter

router = APIRouter(prefix="/login", tags=["login"])


@router.get("/")
async def login():
    return {"message": "Login"}
