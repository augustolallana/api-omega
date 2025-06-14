from fastapi import APIRouter
from starlette import status

from src.schemas.base import BaseResponse

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=BaseResponse)
async def get_cart() -> BaseResponse:
    # Simulate getting cart
    return BaseResponse(
        message="Cart retrieved successfully.",
        status_code=status.HTTP_200_OK,
        detail={"cart": "cart"},
    )


@router.post("/items", response_model=BaseResponse)
async def add_item() -> BaseResponse:
    # Simulate adding item
    return BaseResponse(
        message="Item added successfully.",
        status_code=status.HTTP_201_CREATED,
        cart=None,
        detail={"cart": "cart"},
    )


@router.put("/items/{id}", response_model=BaseResponse)
async def update_item() -> BaseResponse:
    # Simulate updating item
    return BaseResponse(
        message="Item updated successfully.",
        status_code=status.HTTP_200_OK,
        detail={"cart": "cart"},
    )


@router.delete("/items/{id}", response_model=BaseResponse)
async def delete_item() -> BaseResponse:
    # Simulate deleting item
    return BaseResponse(
        message="Item deleted successfully.",
        status_code=status.HTTP_200_OK,
        detail={"cart": "cart"},
    )
