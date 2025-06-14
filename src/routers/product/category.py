from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, and_, func, select
from starlette import status

from src.database.config import get_session
from src.models.product.category import Category
from src.schemas.base import BaseResponse

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=BaseResponse)
async def get_categories(
    session: Session = Depends(get_session),
    name: Optional[str] = Query(
        None,
        description="Filter by category name (case-insensitive partial match)",
    ),
    parent_id: Optional[str] = Query(
        None,
        description="Filter by parent category ID",
    ),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
) -> BaseResponse:
    try:
        # Start with base query
        query = select(Category)

        # Build filter conditions
        conditions = []
        if name:
            conditions.append(Category.name.ilike(f"%{name}%"))
        if parent_id:
            conditions.append(Category.parent_id == parent_id)

        # Apply filters if any exist
        if conditions:
            query = query.where(and_(*conditions))

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        categories = session.exec(query).all()

        # Get total count for pagination
        count_query = select(Category)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        total = session.exec(
            select(func.count()).select_from(count_query.subquery())
        ).first()

        return BaseResponse(
            message="Categories retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters_applied": {
                    "name": name,
                    "parent_id": parent_id,
                },
                "categories": categories,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving categories: {str(e)}",
        )


@router.get("/{id}", response_model=BaseResponse)
async def get_category(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Category).where(Category.id == id)
        category = session.exec(statement).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {id} not found",
            )

        return BaseResponse(
            message="Category retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={"category": category},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving category: {str(e)}",
        )


@router.post("/", response_model=BaseResponse)
async def add_category(
    category: Category, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        # Check if category name already exists
        existing_category = session.exec(
            select(Category).where(Category.name == category.name)
        ).first()

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Category with name '{category.name}' already exists",
            )

        # If parent_id is provided, verify it exists
        if category.parent_id:
            parent = session.exec(
                select(Category).where(Category.id == category.parent_id)
            ).first()
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Parent category with id {category.parent_id} not found",
                )

        session.add(category)
        session.commit()
        session.refresh(category)
        return BaseResponse(
            message="Category added successfully.",
            status_code=status.HTTP_201_CREATED,
            detail={"category": category},
        )
    except HTTPException:
        raise
    except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Category with name '{category.name}' already exists",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding category: {str(e)}",
        )


@router.put("/{id}", response_model=BaseResponse)
async def update_category(
    id: str, category_update: Category, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Category).where(Category.id == id)
        category = session.exec(statement).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {id} not found",
            )

        # Check if new name conflicts with existing category
        if category_update.name != category.name:
            existing_category = session.exec(
                select(Category).where(Category.name == category_update.name)
            ).first()
            if existing_category:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Category with name '{category_update.name}' already exists",
                )

        # If parent_id is being updated, verify it exists and check for circular reference
        if category_update.parent_id != category.parent_id:
            if category_update.parent_id:
                parent = session.exec(
                    select(Category).where(
                        Category.id == category_update.parent_id
                    )
                ).first()
                if not parent:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Parent category with id {category_update.parent_id} not found",
                    )
                # Check for circular reference
                if category_update.parent_id == id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="A category cannot be its own parent",
                    )
                # Check if new parent is not a descendant of this category
                current = parent
                while current.parent_id:
                    if current.parent_id == id:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot set a descendant category as parent (would create a cycle)",
                        )
                    current = session.exec(
                        select(Category).where(
                            Category.id == current.parent_id
                        )
                    ).first()

        for key, value in category_update.model_dump(
            exclude_unset=True
        ).items():
            setattr(category, key, value)

        category.updated_at = datetime.now(timezone.utc)
        session.add(category)
        session.commit()
        session.refresh(category)

        return BaseResponse(
            message="Category updated successfully.",
            status_code=status.HTTP_200_OK,
            detail={"category": category},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating category: {str(e)}",
        )


@router.delete("/{id}", response_model=BaseResponse)
async def delete_category(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Category).where(Category.id == id)
        category = session.exec(statement).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {id} not found",
            )

        # Check if category has associated products
        if category.products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete category with associated products. Please delete or reassign the products first.",
            )

        # Check if category has children
        if category.children:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete category with child categories. Please delete or reassign the children first.",
            )

        session.delete(category)
        session.commit()

        return BaseResponse(
            message="Category deleted successfully.",
            status_code=status.HTTP_200_OK,
            detail={"category_id": id},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting category: {str(e)}",
        )
