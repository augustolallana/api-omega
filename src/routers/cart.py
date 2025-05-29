from fastapi import APIRouter

from src.models.cart import Cart, CartItem, CartResponse

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/")
async def get_cart() -> CartResponse:
    # Get user cart
    c = Cart()
    return CartResponse(
        message="OK.", status_code=200, cart=Cart
    )


@router.post("/items")
async def add_item(cart_item: CartItem) -> Cart:
    # Get user cart
    # Add item to user cart. Validate update quantity
    return {
        "message": "Item added to cart",
        "item": cart_item.model_dump(),
        "cart": "cart",
    }


@router.put("/items/{item_id}")
async def update_item(item_id: str, cart_item: CartItem) -> Cart:
    # Get user cart
    return {
        "message": f"Item updated in cart successfully.",
        "item": cart_item.model_dump(),
        "cart": "cart",
    }


@router.delete("/items/{item_id}")
async def delete_item(item_id: str) -> Cart:
    # Get user cart
    # Get item to delete
    return {
        "message": f"Item deleted from cart successfully.",
        "item": "item",
        "cart": "cart",
    }
