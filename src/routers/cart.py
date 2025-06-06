from fastapi import APIRouter
from starlette import status

from src.schemas.cart import CartResponse

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=CartResponse)
async def get_cart() -> CartResponse:
    # Simulate getting cart
    return CartResponse(
        message="Cart retrieved successfully.",
        status_code=status.HTTP_200_OK,
        cart=None,
    )


@router.post("/items", response_model=CartResponse)
async def add_item() -> CartResponse:
    # Simulate adding item
    return CartResponse(
        message="Item added successfully.",
        status_code=status.HTTP_201_CREATED,
        cart=None,
    )


@router.put("/items/{id}", response_model=CartResponse)
async def update_item() -> CartResponse:
    # Simulate updating item
    return CartResponse(
        message="Item updated successfully.",
        status_code=status.HTTP_200_OK,
        cart=None,
    )


@router.delete("/items/{id}", response_model=CartResponse)
async def delete_item() -> CartResponse:
    # Simulate deleting item
    return CartResponse(
        message="Item deleted successfully.",
        status_code=status.HTTP_200_OK,
        cart=None,
    )
