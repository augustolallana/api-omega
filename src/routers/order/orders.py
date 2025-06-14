from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, and_, func, select
from starlette import status

from src.database.config import get_session
from src.models.order.address import Address
from src.models.order.order import Order
from src.models.order.payment import PaymentMethod, PaymentMethodType
from src.schemas.base import BaseResponse
from src.schemas.order import (
    AddressCreate,
    AddressResponse,
    OrderCreate,
    OrderResponse,
    OrderUpdate,
    PaymentMethodCreate,
    PaymentMethodResponse,
)

order = APIRouter(prefix="/orders", tags=["orders"])


@order.get("/", response_model=BaseResponse)
async def get_orders(
    session: Session = Depends(get_session),
    user_id: Optional[str] = Query(
        None,
        description="Filter by user ID",
    ),
    status: Optional[str] = Query(
        None,
        description="Filter by order status",
    ),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
) -> BaseResponse:
    try:
        # Start with base query
        query = select(Order)

        # Build filter conditions
        conditions = []
        if user_id:
            conditions.append(Order.user_id == user_id)
        if status:
            conditions.append(Order.status == status)

        # Apply filters if any exist
        if conditions:
            query = query.where(and_(*conditions))

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        orders = session.exec(query).all()

        # Get total count for pagination
        count_query = select(Order)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        total = session.exec(
            select(func.count()).select_from(count_query.subquery())
        ).first()

        return BaseResponse(
            message="Orders retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters_applied": {
                    "user_id": user_id,
                    "status": status,
                },
                "orders": orders,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving orders: {str(e)}",
        )


@order.get("/{id}", response_model=BaseResponse)
async def get_order(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Order).where(Order.id == id)
        order = session.exec(statement).first()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {id} not found",
            )

        return BaseResponse(
            message="Order retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={"order": order},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving order: {str(e)}",
        )


@order.post("/", response_model=BaseResponse)
async def create_order(
    order_data: OrderCreate, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        # Validate address exists
        address = session.exec(
            select(Address).where(Address.id == order_data.address_id)
        ).first()
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Address with id {order_data.address_id} not found",
            )

        # Validate payment method exists
        payment_method = session.exec(
            select(PaymentMethod).where(
                PaymentMethod.id == order_data.payment_method_id
            )
        ).first()
        if not payment_method:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment method with id {order_data.payment_method_id} not found",
            )

        # Create order
        order = Order(
            user_id=order_data.user_id,
            address_id=order_data.address_id,
            payment_method_id=order_data.payment_method_id,
            total_amount=order_data.total_amount,
            status="pending",
        )

        session.add(order)
        session.commit()
        session.refresh(order)

        return BaseResponse(
            message="Order created successfully.",
            status_code=status.HTTP_201_CREATED,
            detail={"order": order},
        )
    except HTTPException:
        raise
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating order: {str(e)}",
        )


@order.put("/{id}", response_model=BaseResponse)
async def update_order(
    id: str,
    order_update: OrderUpdate,
    session: Session = Depends(get_session),
) -> BaseResponse:
    try:
        statement = select(Order).where(Order.id == id)
        order = session.exec(statement).first()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {id} not found",
            )

        # Validate address if being updated
        if (
            order_update.address_id
            and order_update.address_id != order.address_id
        ):
            address = session.exec(
                select(Address).where(Address.id == order_update.address_id)
            ).first()
            if not address:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Address with id {order_update.address_id} not found",
                )

        # Validate payment method if being updated
        if (
            order_update.payment_method_id
            and order_update.payment_method_id != order.payment_method_id
        ):
            payment_method = session.exec(
                select(PaymentMethod).where(
                    PaymentMethod.id == order_update.payment_method_id
                )
            ).first()
            if not payment_method:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Payment method with id {order_update.payment_method_id} not found",
                )

        # Update order
        for key, value in order_update.model_dump(exclude_unset=True).items():
            setattr(order, key, value)

        order.updated_at = datetime.now(timezone.utc)
        session.add(order)
        session.commit()
        session.refresh(order)

        return BaseResponse(
            message="Order updated successfully.",
            status_code=status.HTTP_200_OK,
            detail={"order": order},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating order: {str(e)}",
        )


@order.delete("/{id}", response_model=BaseResponse)
async def delete_order(
    id: str, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        statement = select(Order).where(Order.id == id)
        order = session.exec(statement).first()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {id} not found",
            )

        # Check if order can be deleted (e.g., only if status is 'pending')
        if order.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending orders can be deleted",
            )

        session.delete(order)
        session.commit()

        return BaseResponse(
            message="Order deleted successfully.",
            status_code=status.HTTP_200_OK,
            detail={"order_id": id},
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting order: {str(e)}",
        )
