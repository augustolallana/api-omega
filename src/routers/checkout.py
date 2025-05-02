from fastapi import APIRouter

router = APIRouter(prefix="/checkout", tags=["checkout"])


@router.get("/")
async def checkout():
    return {"message": "checkout"}
