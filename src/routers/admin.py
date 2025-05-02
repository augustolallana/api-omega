from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/")
async def admin():
    return {"message": "Login"}
