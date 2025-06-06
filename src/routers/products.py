from fastapi import APIRouter
from starlette import status

"""
NOTE 
from fastapi import Query
Query object has attribute pattern that allows for regex
over query parameters
"""

from src.models import Product
from src.schemas import ProductListResponse, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=ProductListResponse)
async def get_products() -> ProductListResponse:
    # Retrieve from db
    products = []
    return ProductListResponse(
        message="Ok.", status_code=status.HTTP_200_OK, products=products
    )


@router.post("/", response_model=ProductResponse)
async def add_product(product: Product) -> ProductResponse:
    # Add to db
    return ProductResponse(
        message="Product added successfully.",
        status_code=status.HTTP_201_CREATED,
        product=product,
    )


@router.put("/{id}", response_model=ProductResponse)
async def update_product(product: Product) -> ProductResponse:
    # Retrieve from db
    # Simulate old_product = ...
    return ProductResponse(
        message="Product updated successfully.",
        status_code=status.HTTP_200_OK,
        product=product,
    )


@router.delete("/{id}", response_model=ProductResponse)
async def delete_product(id: str) -> ProductResponse:
    # Remove from db
    # Simulate old_product = ...
    return ProductResponse(
        message="Product deleted successfully.",
        status_code=status.HTTP_200_OK,
        product=None,
    )
