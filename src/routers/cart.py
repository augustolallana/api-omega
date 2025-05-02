from fastapi import APIRouter

from src.models.cart import Cart

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/")
async def get_cart() -> Cart:
    return {"message": "Get cart items"}


@router.post("/items")
async def add_item() -> Cart:
    return {"message": "Add item to cart"}


@router.put("/items/{item_id}")
async def update_item(item_id: int) -> Cart:
    return {"message": f"Update item {item_id} in cart"}


@router.delete("/items/{item_id}")
async def delete_item(item_id: int) -> Cart:
    return {"message": f"Remove item {item_id} from cart"}
