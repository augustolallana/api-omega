from fastapi import APIRouter

"""
NOTE 
from fastapi import Query
Query object has attribute pattern that allows for regex
over query parameters
"""

from src.models.product import Product

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
async def get_products():
    # Retrieve from db
    return {"message": "Ok.", "products": "products"}


@router.post("/")
async def add_product(product: Product) -> Product:
    # Add to db
    return {
        "message": "Product added successfully.",
        "product": product.model_dump(),
    }


@router.put("/{id}")
async def update_product(product: Product) -> Product:
    # Retrieve from db
    return {
        "message": "Product updated successfully.",
        "new_product": product.model_dump(),
        "old_product": "old_product",
    }


@router.delete("/{id}")
async def delete_product(id: str) -> Product:
    # Remove from db
    return {
        "message": "Product deleted successfully.",
        "old_product": "old_product",
    }
