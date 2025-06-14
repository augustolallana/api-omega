from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, and_, func, select
from starlette import status

from src.database.config import get_session
from src.models.product.brand import Brand
from src.schemas.base import BaseResponse

router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("/", response_model=BaseResponse)
async def get_brands(
    session: Session = Depends(get_session),
    name: Optional[str] = Query(
        None,
        description="Filter by brand name (case-insensitive partial match)",
    ),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
) -> BaseResponse:
    try:
        # Start with base query
        query = select(Brand)

        # Build filter conditions
        conditions = []
        if name:
            conditions.append(Brand.name.ilike(f"%{name}%"))

        # Apply filters if any exist
        if conditions:
            query = query.where(and_(*conditions))

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        brands = session.exec(query).all()

        # Get total count for pagination
        count_query = select(Brand)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        total = session.exec(
            select(func.count()).select_from(count_query.subquery())
        ).first()

        return BaseResponse(
            message="Brands retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters_applied": {
                    "name": name,
                },
                "brands": brands,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving brands: {str(e)}",
        )


@router.get("/{id}", response_model=BaseResponse)
async def get_brand(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Brand).where(Brand.id == id)
        brand = session.exec(statement).first()

        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Brand with id {id} not found",
            )

        return BaseResponse(
            message="Brand retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={"brand": brand},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving brand: {str(e)}",
        )


@router.post("/", response_model=BaseResponse)
async def add_brand(
    brand: Brand, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        # Check if brand name already exists
        existing_brand = session.exec(
            select(Brand).where(Brand.name == brand.name)
        ).first()

        if existing_brand:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Brand with name '{brand.name}' already exists",
            )

        session.add(brand)
        session.commit()
        session.refresh(brand)
        return BaseResponse(
            message="Brand added successfully.",
            status_code=status.HTTP_201_CREATED,
            detail={"brand": brand},
        )
    except HTTPException:
        raise
    except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Brand with name '{brand.name}' already exists",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding brand: {str(e)}",
        )


@router.put("/{id}", response_model=BaseResponse)
async def update_brand(
    id: str, brand_update: Brand, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Brand).where(Brand.id == id)
        brand = session.exec(statement).first()

        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Brand with id {id} not found",
            )

        # Check if new name conflicts with existing brand
        if brand_update.name != brand.name:
            existing_brand = session.exec(
                select(Brand).where(Brand.name == brand_update.name)
            ).first()
            if existing_brand:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Brand with name '{brand_update.name}' already exists",
                )

        for key, value in brand_update.model_dump(exclude_unset=True).items():
            setattr(brand, key, value)

        brand.updated_at = datetime.now(timezone.utc)
        session.add(brand)
        session.commit()
        session.refresh(brand)

        return BaseResponse(
            message="Brand updated successfully.",
            status_code=status.HTTP_200_OK,
            detail={"brand": brand},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating brand: {str(e)}",
        )


@router.delete("/{id}", response_model=BaseResponse)
async def delete_brand(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Brand).where(Brand.id == id)
        brand = session.exec(statement).first()

        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Brand with id {id} not found",
            )

        # Check if brand has associated products
        if brand.products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete brand with associated products. Please delete or reassign the products first.",
            )

        session.delete(brand)
        session.commit()

        return BaseResponse(
            message="Brand deleted successfully.",
            status_code=status.HTTP_200_OK,
            detail={"brand_id": id},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting brand: {str(e)}",
        )
