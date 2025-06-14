from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, and_, func, select
from starlette import status

"""
NOTE 
from fastapi import Query
Query object has attribute pattern that allows for regex
over query parameters
"""

from src.database.config import get_session
from src.models.product.product import Product
from src.schemas.base import BaseResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=BaseResponse)
async def get_products(
    session: Session = Depends(get_session),
    name: Optional[str] = Query(
        None,
        description="Filter by product name (case-insensitive partial match)",
    ),
    min_price: Optional[float] = Query(
        None, description="Filter by minimum price"
    ),
    max_price: Optional[float] = Query(
        None, description="Filter by maximum price"
    ),
    category_id: Optional[str] = Query(
        None, description="Filter by category ID"
    ),
    brand_id: Optional[str] = Query(None, description="Filter by brand ID"),
    min_stock: Optional[int] = Query(
        None, description="Filter by minimum stock"
    ),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
) -> BaseResponse:
    try:
        # Start with base query
        query = select(Product)

        # Build filter conditions
        conditions = []
        if name:
            conditions.append(Product.name.ilike(f"%{name}%"))
        if min_price is not None:
            conditions.append(Product.price >= min_price)
        if max_price is not None:
            conditions.append(Product.price <= max_price)
        if category_id:
            conditions.append(Product.category_id == category_id)
        if brand_id:
            conditions.append(Product.brand_id == brand_id)
        if min_stock is not None:
            conditions.append(Product.stock >= min_stock)

        # Apply filters if any exist
        if conditions:
            query = query.where(and_(*conditions))

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        products = session.exec(query).all()

        # Get total count for pagination
        count_query = select(Product)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        total = session.exec(
            select(func.count()).select_from(count_query.subquery())
        ).first()

        return BaseResponse(
            message="Products retrieved successfully.",
            status_code=status.HTTP_200_OK,
            products=products,
            detail={
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters_applied": {
                    "name": name,
                    "min_price": min_price,
                    "max_price": max_price,
                    "category_id": category_id,
                    "brand_id": brand_id,
                    "min_stock": min_stock,
                },
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving products: {str(e)}",
        )


@router.get("/{id}", response_model=BaseResponse)
async def get_product(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Product).where(Product.id == id)
        product = session.exec(statement).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {id} not found",
            )

        return BaseResponse(
            message="Product retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={"product": product},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving product: {str(e)}",
        )


@router.post("/", response_model=BaseResponse)
async def add_product(
    product: Product, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        # Check if product name already exists
        existing_product = session.exec(
            select(Product).where(Product.name == product.name)
        ).first()

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Product with name '{product.name}' already exists",
            )

        session.add(product)
        session.commit()
        session.refresh(product)
        return BaseResponse(
            message="Product added successfully.",
            status_code=status.HTTP_201_CREATED,
            detail={"product": product},
        )
    except HTTPException:
        raise
    except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Product with name '{product.name}' already exists",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding product: {str(e)}",
        )


@router.put("/{id}", response_model=BaseResponse)
async def update_product(
    id: str, product_update: Product, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Product).where(Product.id == id)
        product = session.exec(statement).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {id} not found",
            )

        for key, value in product_update.dict(exclude_unset=True).items():
            setattr(product, key, value)

        product.updated_at = datetime.now(timezone.utc)
        session.add(product)
        session.commit()
        session.refresh(product)

        return BaseResponse(
            message="Product updated successfully.",
            status_code=status.HTTP_200_OK,
            detail={"product": product},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating product: {str(e)}",
        )


@router.delete("/{id}", response_model=BaseResponse)
async def delete_product(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Product).where(Product.id == id)
        product = session.exec(statement).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {id} not found",
            )

        session.delete(product)
        session.commit()

        return BaseResponse(
            message="Product deleted successfully.",
            status_code=status.HTTP_200_OK,
            detail={"product_id": id},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting product: {str(e)}",
        )
