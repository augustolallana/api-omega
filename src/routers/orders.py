from fastapi import APIRouter

router = APIRouter(prefix="/oders", tags=["orders"])


@router.get("/")
async def get_orders():
    return {"message": "orders"}
