from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, and_, func, select

from src.database.config import get_session
from src.models.product.product import Product
from src.schemas.base import BaseResponse
from src.schemas.products.product import ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=BaseResponse)
async def get_products(
    session: Session = Depends(get_session),
    name: Optional[str] = Query(
        None,
        description="Filter by product name (case-insensitive partial match)",
    ),
    category_id: Optional[str] = Query(
        None,
        description="Filter by category ID",
    ),
    brand_id: Optional[str] = Query(
        None,
        description="Filter by brand ID",
    ),
    min_price: Optional[float] = Query(
        None,
        description="Filter by minimum price",
    ),
    max_price: Optional[float] = Query(
        None,
        description="Filter by maximum price",
    ),
    in_stock: Optional[bool] = Query(
        None,
        description="Filter by stock availability",
    ),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
) -> BaseResponse:
    try:
        # Start with base query
        query = select(Product)

        # Build filter conditions
        conditions = []
        if name:
            conditions.append(Product.name.ilike(f"%{name}%"))
        if category_id:
            conditions.append(Product.category_id == category_id)
        if brand_id:
            conditions.append(Product.brand_id == brand_id)
        if min_price is not None:
            conditions.append(Product.price >= min_price)
        if max_price is not None:
            conditions.append(Product.price <= max_price)
        if in_stock is not None:
            if in_stock:
                conditions.append(Product.stock > 0)
            else:
                conditions.append(Product.stock == 0)

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
            detail={
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters_applied": {
                    "name": name,
                    "category_id": category_id,
                    "brand_id": brand_id,
                    "min_price": min_price,
                    "max_price": max_price,
                    "in_stock": in_stock,
                },
                "products": products,
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
async def create_product(
    product_create: ProductCreate, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        # Check if product with same name already exists
        existing_product = session.exec(
            select(Product).where(Product.name == product_create.name)
        ).first()
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Product with name '{product_create.name}' already exists",
            )

        # Verify category exists
        category = session.exec(
            select(Product).where(
                Product.category_id == product_create.category_id
            )
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {product_create.category_id} not found",
            )

        # Verify brand exists
        brand = session.exec(
            select(Product).where(Product.brand_id == product_create.brand_id)
        ).first()
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Brand with id {product_create.brand_id} not found",
            )

        product = Product(**product_create.model_dump())
        session.add(product)
        session.commit()
        session.refresh(product)

        return BaseResponse(
            message="Product created successfully.",
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
                detail=f"Product with name '{product_create.name}' already exists",
            )
        if "foreign key constraint" in str(e).lower():
            if "category_id" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with id {product_create.category_id} not found",
                )
            if "brand_id" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Brand with id {product_create.brand_id} not found",
                )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}",
        )


@router.put("/{id}", response_model=BaseResponse)
async def update_product(
    id: str,
    product_update: ProductUpdate,
    session: Session = Depends(get_session),
) -> BaseResponse:
    try:
        statement = select(Product).where(Product.id == id)
        product = session.exec(statement).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {id} not found",
            )

        # Check if new name conflicts with existing product
        if product_update.name and product_update.name != product.name:
            existing_product = session.exec(
                select(Product).where(Product.name == product_update.name)
            ).first()
            if existing_product:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Product with name '{product_update.name}' already exists",
                )

        # If category_id is being updated, verify it exists
        if (
            product_update.category_id
            and product_update.category_id != product.category_id
        ):
            category = session.exec(
                select(Product).where(
                    Product.category_id == product_update.category_id
                )
            ).first()
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with id {product_update.category_id} not found",
                )

        # If brand_id is being updated, verify it exists
        if (
            product_update.brand_id
            and product_update.brand_id != product.brand_id
        ):
            brand = session.exec(
                select(Product).where(
                    Product.brand_id == product_update.brand_id
                )
            ).first()
            if not brand:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Brand with id {product_update.brand_id} not found",
                )

        for key, value in product_update.model_dump(
            exclude_unset=True
        ).items():
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

        # Check if product has associated cart items
        if product.cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete product with associated cart items. Please remove the product from carts first.",
            )

        # Check if product has associated order items
        if product.order_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete product with associated order items. Please remove the product from orders first.",
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
