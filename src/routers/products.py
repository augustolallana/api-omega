from fastapi import APIRouter
from starlette import status

"""
NOTE 
from fastapi import Query
Query object has attribute pattern that allows for regex
over query parameters
"""

from src.models.product.product import Product
from src.schemas.base import BaseResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=BaseResponse)
async def get_products() -> BaseResponse:
    # Retrieve from db
    products = []
    return BaseResponse(
        message="Ok.", status_code=status.HTTP_200_OK, products=products
    )


@router.post("/", response_model=BaseResponse)
async def add_product(product: Product) -> BaseResponse:
    # Add to db
    return BaseResponse(
        message="Product added successfully.",
        status_code=status.HTTP_201_CREATED,
        detail={"product": product},
    )


@router.put("/{id}", response_model=BaseResponse)
async def update_product(product: Product) -> BaseResponse:
    # Retrieve from db
    # Simulate old_product = ...
    return BaseResponse(
        message="Product updated successfully.",
        status_code=status.HTTP_200_OK,
        detail={"product": product},
    )


@router.delete("/{id}", response_model=BaseResponse)
async def delete_product(id: str) -> BaseResponse:
    # Remove from db
    # Simulate old_product = ...
    return BaseResponse(
        message="Product deleted successfully.",
        status_code=status.HTTP_200_OK,
        detail={"product.id": "product.id"},
    )
