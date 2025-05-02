from fastapi import APIRouter

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/")
async def get_cart():
    return {"message": "Get cart items"}
