from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, and_, func, select
from starlette import status

from src.database.config import get_session
from src.models.product.tag import Tag
from src.schemas.base import BaseResponse

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=BaseResponse)
async def get_tags(
    session: Session = Depends(get_session),
    name: Optional[str] = Query(
        None,
        description="Filter by tag name (case-insensitive partial match)",
    ),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
) -> BaseResponse:
    try:
        # Start with base query
        query = select(Tag)

        # Build filter conditions
        conditions = []
        if name:
            conditions.append(Tag.name.ilike(f"%{name}%"))

        # Apply filters if any exist
        if conditions:
            query = query.where(and_(*conditions))

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        tags = session.exec(query).all()

        # Get total count for pagination
        count_query = select(Tag)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        total = session.exec(
            select(func.count()).select_from(count_query.subquery())
        ).first()

        return BaseResponse(
            message="Tags retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters_applied": {
                    "name": name,
                },
                "tags": tags,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tags: {str(e)}",
        )


@router.get("/{id}", response_model=BaseResponse)
async def get_tag(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Tag).where(Tag.id == id)
        tag = session.exec(statement).first()

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag with id {id} not found",
            )

        return BaseResponse(
            message="Tag retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={"tag": tag},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tag: {str(e)}",
        )


@router.post("/", response_model=BaseResponse)
async def add_tag(
    tag: Tag, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        # Check if tag name already exists
        existing_tag = session.exec(
            select(Tag).where(Tag.name == tag.name)
        ).first()

        if existing_tag:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tag with name '{tag.name}' already exists",
            )

        session.add(tag)
        session.commit()
        session.refresh(tag)
        return BaseResponse(
            message="Tag added successfully.",
            status_code=status.HTTP_201_CREATED,
            detail={"tag": tag},
        )
    except HTTPException:
        raise
    except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tag with name '{tag.name}' already exists",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding tag: {str(e)}",
        )


@router.put("/{id}", response_model=BaseResponse)
async def update_tag(
    id: str, tag_update: Tag, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Tag).where(Tag.id == id)
        tag = session.exec(statement).first()

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag with id {id} not found",
            )

        # Check if new name conflicts with existing tag
        if tag_update.name != tag.name:
            existing_tag = session.exec(
                select(Tag).where(Tag.name == tag_update.name)
            ).first()
            if existing_tag:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Tag with name '{tag_update.name}' already exists",
                )

        for key, value in tag_update.model_dump(exclude_unset=True).items():
            setattr(tag, key, value)

        tag.updated_at = datetime.now(timezone.utc)
        session.add(tag)
        session.commit()
        session.refresh(tag)

        return BaseResponse(
            message="Tag updated successfully.",
            status_code=status.HTTP_200_OK,
            detail={"tag": tag},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating tag: {str(e)}",
        )


@router.delete("/{id}", response_model=BaseResponse)
async def delete_tag(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Tag).where(Tag.id == id)
        tag = session.exec(statement).first()

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag with id {id} not found",
            )

        # Check if tag has associated products
        if tag.products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete tag with associated products. Please remove the products first.",
            )

        session.delete(tag)
        session.commit()

        return BaseResponse(
            message="Tag deleted successfully.",
            status_code=status.HTTP_200_OK,
            detail={"tag_id": id},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting tag: {str(e)}",
        )
