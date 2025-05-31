from fastapi import APIRouter
from starlette import status

from src.models.cart import Cart, CartItem, CartResponse

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=CartResponse)
async def get_cart() -> CartResponse:
    c = Cart(id="cart-1", items=[])
    return CartResponse(message="OK.", status_code=status.HTTP_200_OK, cart=c)


@router.post("/items", response_model=CartResponse)
async def add_item(cart_item: CartItem) -> CartResponse:
    # Simular cart actualizado
    c = Cart(id="cart-1", items=[cart_item])
    return CartResponse(
        message="Item added to cart.",
        status_code=status.HTTP_200_OK,
        item=cart_item,
        cart=c,
    )


@router.put("/items/{item_id}", response_model=CartResponse)
async def update_item(item_id: str, cart_item: CartItem) -> CartResponse:
    c = Cart(id="cart-1", items=[cart_item])
    return CartResponse(
        message="Item updated in cart successfully.",
        status_code=status.HTTP_200_OK,
        item=cart_item,
        cart=c,
    )


@router.delete("/items/{item_id}", response_model=CartResponse)
async def delete_item(item_id: str) -> CartResponse:
    c = Cart(id="cart-1", items=[])
    return CartResponse(
        message="Item removed from cart successfully.",
        status_code=status.HTTP_200_OK,
        cart=c,
    )
