from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, and_, func, select

from src.database.config import get_session
from src.models.product.promotion import Promotion
from src.schemas.base import BaseResponse
from src.schemas.products.promotion import PromotionCreate, PromotionUpdate

router = APIRouter(prefix="/promotions", tags=["promotions"])


@router.get("/", response_model=BaseResponse)
async def get_promotions(
    session: Session = Depends(get_session),
    name: Optional[str] = Query(
        None,
        description="Filter by promotion name (case-insensitive partial match)",
    ),
    active: Optional[bool] = Query(
        None,
        description="Filter by active status (based on current date)",
    ),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
) -> BaseResponse:
    try:
        # Start with base query
        query = select(Promotion)

        # Build filter conditions
        conditions = []
        if name:
            conditions.append(Promotion.name.ilike(f"%{name}%"))
        if active is not None:
            now = datetime.now(timezone.utc)
            if active:
                conditions.append(Promotion.start_date <= now)
                conditions.append(Promotion.end_date >= now)
            else:
                conditions.append(
                    (Promotion.start_date > now) | (Promotion.end_date < now)
                )

        # Apply filters if any exist
        if conditions:
            query = query.where(and_(*conditions))

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        promotions = session.exec(query).all()

        # Get total count for pagination
        count_query = select(Promotion)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        total = session.exec(
            select(func.count()).select_from(count_query.subquery())
        ).first()

        return BaseResponse(
            message="Promotions retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters_applied": {
                    "name": name,
                    "active": active,
                },
                "promotions": promotions,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving promotions: {str(e)}",
        )


@router.get("/{id}", response_model=BaseResponse)
async def get_promotion(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Promotion).where(Promotion.id == id)
        promotion = session.exec(statement).first()

        if not promotion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Promotion with id {id} not found",
            )

        return BaseResponse(
            message="Promotion retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={"promotion": promotion},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving promotion: {str(e)}",
        )


@router.post("/", response_model=BaseResponse)
async def create_promotion(
    promotion_create: PromotionCreate, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        # Check if promotion with same name already exists
        existing_promotion = session.exec(
            select(Promotion).where(Promotion.name == promotion_create.name)
        ).first()
        if existing_promotion:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Promotion with name '{promotion_create.name}' already exists",
            )

        # Validate dates
        if promotion_create.start_date >= promotion_create.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date must be before end date",
            )

        promotion = Promotion(**promotion_create.model_dump())
        session.add(promotion)
        session.commit()
        session.refresh(promotion)

        return BaseResponse(
            message="Promotion created successfully.",
            status_code=status.HTTP_201_CREATED,
            detail={"promotion": promotion},
        )
    except HTTPException:
        raise
    except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Promotion with name '{promotion_create.name}' already exists",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating promotion: {str(e)}",
        )


@router.put("/{id}", response_model=BaseResponse)
async def update_promotion(
    id: str,
    promotion_update: PromotionUpdate,
    session: Session = Depends(get_session),
) -> BaseResponse:
    try:
        statement = select(Promotion).where(Promotion.id == id)
        promotion = session.exec(statement).first()

        if not promotion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Promotion with id {id} not found",
            )

        # Check if new name conflicts with existing promotion
        if promotion_update.name and promotion_update.name != promotion.name:
            existing_promotion = session.exec(
                select(Promotion).where(
                    Promotion.name == promotion_update.name
                )
            ).first()
            if existing_promotion:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Promotion with name '{promotion_update.name}' already exists",
                )

        # Validate dates if being updated
        if promotion_update.start_date and promotion_update.end_date:
            if promotion_update.start_date >= promotion_update.end_date:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Start date must be before end date",
                )
        elif promotion_update.start_date:
            if promotion_update.start_date >= promotion.end_date:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Start date must be before end date",
                )
        elif promotion_update.end_date:
            if promotion.start_date >= promotion_update.end_date:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Start date must be before end date",
                )

        for key, value in promotion_update.model_dump(
            exclude_unset=True
        ).items():
            setattr(promotion, key, value)

        promotion.updated_at = datetime.now(timezone.utc)
        session.add(promotion)
        session.commit()
        session.refresh(promotion)

        return BaseResponse(
            message="Promotion updated successfully.",
            status_code=status.HTTP_200_OK,
            detail={"promotion": promotion},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating promotion: {str(e)}",
        )


@router.delete("/{id}", response_model=BaseResponse)
async def delete_promotion(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Promotion).where(Promotion.id == id)
        promotion = session.exec(statement).first()

        if not promotion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Promotion with id {id} not found",
            )

        # Check if promotion has associated products
        if promotion.products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete promotion with associated products. Please remove the promotion from products first.",
            )

        session.delete(promotion)
        session.commit()

        return BaseResponse(
            message="Promotion deleted successfully.",
            status_code=status.HTTP_200_OK,
            detail={"promotion_id": id},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting promotion: {str(e)}",
        )
