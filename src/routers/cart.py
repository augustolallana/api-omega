from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, and_, func, select

from src.database.config import get_session
from src.models.cart.cart import CartItem
from src.models.product.product import Product
from src.schemas.base import BaseResponse
from src.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=BaseResponse)
async def get_cart(
    session: Session = Depends(get_session),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
) -> BaseResponse:
    try:
        # Get cart items with product details
        query = (
            select(CartItem, Product)
            .join(Product)
            .offset(skip)
            .limit(limit)
        )
        results = session.exec(query).all()

        # Calculate totals
        total_items = sum(item.quantity for item, _ in results)
        total_price = sum(item.quantity * product.current_price for item, product in results)

        # Format response
        cart_items = [
            CartItemResponse(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item, _ in results
        ]

        cart_response = CartResponse(
            items=cart_items,
            total_items=total_items,
            total_price=total_price,
        )

        return BaseResponse(
            message="Cart retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={"cart": cart_response},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving cart: {str(e)}",
        )


@router.post("/items", response_model=BaseResponse)
async def add_item(
    cart_item: CartItemCreate, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        # Verify product exists and has enough stock
        product = session.exec(
            select(Product).where(Product.id == cart_item.product_id)
        ).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {cart_item.product_id} not found",
            )
        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock available. Only {product.stock} items left.",
            )

        # Check if item already exists in cart
        existing_item = session.exec(
            select(CartItem).where(CartItem.product_id == cart_item.product_id)
        ).first()

        if existing_item:
            # Update quantity if item exists
            new_quantity = existing_item.quantity + cart_item.quantity
            if new_quantity > product.stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough stock available. Only {product.stock} items left.",
                )
            existing_item.quantity = new_quantity
            session.add(existing_item)
        else:
            # Create new cart item
            cart_item_db = CartItem(**cart_item.model_dump())
            session.add(cart_item_db)

        session.commit()
        if existing_item:
            session.refresh(existing_item)
            return BaseResponse(
                message="Cart item quantity updated successfully.",
                status_code=status.HTTP_200_OK,
                detail={"cart_item": existing_item},
            )
        else:
            session.refresh(cart_item_db)
            return BaseResponse(
                message="Item added to cart successfully.",
                status_code=status.HTTP_201_CREATED,
                detail={"cart_item": cart_item_db},
            )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding item to cart: {str(e)}",
        )


@router.put("/items/{id}", response_model=BaseResponse)
async def update_item(
    id: UUID,
    cart_item_update: CartItemUpdate,
    session: Session = Depends(get_session),
) -> BaseResponse:
    try:
        # Get cart item
        cart_item = session.exec(
            select(CartItem).where(CartItem.id == id)
        ).first()
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cart item with id {id} not found",
            )

        # Verify product has enough stock
        product = session.exec(
            select(Product).where(Product.id == cart_item.product_id)
        ).first()
        if product.stock < cart_item_update.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock available. Only {product.stock} items left.",
            )

        # Update quantity
        cart_item.quantity = cart_item_update.quantity
        session.add(cart_item)
        session.commit()
        session.refresh(cart_item)

        return BaseResponse(
            message="Cart item updated successfully.",
            status_code=status.HTTP_200_OK,
            detail={"cart_item": cart_item},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating cart item: {str(e)}",
        )


@router.delete("/items/{id}", response_model=BaseResponse)
async def delete_item(
    id: UUID, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        # Get cart item
        cart_item = session.exec(
            select(CartItem).where(CartItem.id == id)
        ).first()
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cart item with id {id} not found",
            )

        # Delete item
        session.delete(cart_item)
        session.commit()

        return BaseResponse(
            message="Cart item deleted successfully.",
            status_code=status.HTTP_200_OK,
            detail={"cart_item_id": id},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting cart item: {str(e)}",
        )
