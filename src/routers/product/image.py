from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, and_, func, select

from src.database.config import get_session
from src.models.product.image import Image
from src.schemas.base import BaseResponse
from src.schemas.products.image import ImageCreate, ImageUpdate

router = APIRouter(prefix="/images", tags=["images"])


@router.get("/", response_model=BaseResponse)
async def get_images(
    session: Session = Depends(get_session),
    product_id: Optional[str] = Query(
        None,
        description="Filter by product ID",
    ),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
) -> BaseResponse:
    try:
        # Start with base query
        query = select(Image)

        # Build filter conditions
        conditions = []
        if product_id:
            conditions.append(Image.product_id == product_id)

        # Apply filters if any exist
        if conditions:
            query = query.where(and_(*conditions))

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        images = session.exec(query).all()

        # Get total count for pagination
        count_query = select(Image)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        total = session.exec(
            select(func.count()).select_from(count_query.subquery())
        ).first()

        return BaseResponse(
            message="Images retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters_applied": {
                    "product_id": product_id,
                },
                "images": images,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving images: {str(e)}",
        )


@router.get("/{id}", response_model=BaseResponse)
async def get_image(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Image).where(Image.id == id)
        image = session.exec(statement).first()

        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Image with id {id} not found",
            )

        return BaseResponse(
            message="Image retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={"image": image},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving image: {str(e)}",
        )


@router.post("/", response_model=BaseResponse)
async def create_image(
    image_create: ImageCreate, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        # Check if product exists
        product = session.exec(
            select(Image).where(Image.product_id == image_create.product_id)
        ).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {image_create.product_id} not found",
            )

        image = Image(**image_create.model_dump())
        session.add(image)
        session.commit()
        session.refresh(image)

        return BaseResponse(
            message="Image created successfully.",
            status_code=status.HTTP_201_CREATED,
            detail={"image": image},
        )
    except HTTPException:
        raise
    except IntegrityError as e:
        session.rollback()
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {image_create.product_id} not found",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating image: {str(e)}",
        )


@router.put("/{id}", response_model=BaseResponse)
async def update_image(
    id: str, image_update: ImageUpdate, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Image).where(Image.id == id)
        image = session.exec(statement).first()

        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Image with id {id} not found",
            )

        for key, value in image_update.model_dump(exclude_unset=True).items():
            setattr(image, key, value)

        image.updated_at = datetime.now(timezone.utc)
        session.add(image)
        session.commit()
        session.refresh(image)

        return BaseResponse(
            message="Image updated successfully.",
            status_code=status.HTTP_200_OK,
            detail={"image": image},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating image: {str(e)}",
        )


@router.delete("/{id}", response_model=BaseResponse)
async def delete_image(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Image).where(Image.id == id)
        image = session.exec(statement).first()

        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Image with id {id} not found",
            )

        session.delete(image)
        session.commit()

        return BaseResponse(
            message="Image deleted successfully.",
            status_code=status.HTTP_200_OK,
            detail={"image_id": id},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting image: {str(e)}",
        )
