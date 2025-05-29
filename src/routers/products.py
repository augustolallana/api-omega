from fastapi import APIRouter
from starlette import status

"""
NOTE 
from fastapi import Query
Query object has attribute pattern that allows for regex
over query parameters
"""

from src.models.base_response import BaseResponse
from src.models.product import Product, ProductsResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=BaseResponse)
async def get_products() -> ProductsResponse:
    # Retrieve from db
    products = []
    return ProductsResponse(
        message="Ok.", status_code=status.HTTP_200_OK, products=products
    )


@router.post("/", response_model=ProductsResponse)
async def add_product(product: Product) -> ProductsResponse:
    # Add to db
    return ProductsResponse(
        message="Product added successfully.",
        status_code=status.HTTP_201_CREATED,
        new_product=product,
        old_product=None,
    )


@router.put("/{id}", response_model=ProductsResponse)
async def update_product(product: Product) -> ProductsResponse:
    # Retrieve from db
    # Simulate old_product = ...
    return ProductsResponse(
        message="Product updated successfully.",
        status_code=status.HTTP_200_OK,
        new_product=product,
        old_product=None,  # Replace with actual old product
    )


@router.delete("/{id}", response_model=ProductsResponse)
async def delete_product(id: str) -> ProductsResponse:
    # Remove from db
    # Simulate old_product = ...
    return ProductsResponse(
        message="Product deleted successfully.",
        status_code=status.HTTP_200_OK,
        old_product=None,
        new_product=None,
    )
