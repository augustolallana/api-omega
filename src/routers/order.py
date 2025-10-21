from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from src.database.config import get_session, get_current_user
from src.models.order.order import Order
from src.models.order.order_item import OrderItem
from src.models.order.payment import PaymentMethod
from src.models.product.product import Product
from src.models.user import User
from src.schemas.base import BaseResponse
from src.schemas.order import (
    OrderCreate,
    OrderResponse,
)

router = APIRouter(prefix="/order", tags=["order"])


@router.get("/{id}", response_model=BaseResponse)
async def get_order_by_id(
    id: str,
    session: Session = Depends(get_session),
) -> BaseResponse:
    try:
        order = session.exec(select(Order).where(Order.id == id)).first()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id '{id}' not found",
            )

        order_response = OrderResponse(
            id=order.id,
            user_id=order.user_id,
            address_id=order.address_id,
            payment_method_id=order.payment_method_id,
            total_amount=order.total_amount,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=list(order.items),
            address=order.address,
            payment_method=order.payment_method.type,
        )

        return BaseResponse(
            message="Order retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={"order": order_response},
        )

    except Exception as e:
        raise HTTPException(
            status_code=(
                e.status_code
                if hasattr(e, "status_code")
                else status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=f"Error retrieving order: {str(e.detail) if hasattr(e, 'detail') else str(e)}",
        )


@router.get("/user/{id}", response_model=BaseResponse)
async def get_all_user_orders(
    id: str,
    session: Session = Depends(get_session),
    auth=Depends(get_current_user)
) -> BaseResponse:
    try:
        all_orders = session.exec(select(Order).where(Order.user_id == id)).all()

        if not all_orders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id '{id}' has no orders",
            )

        orders_response = [
            OrderResponse(
                id=order.id,
                user_id=order.user_id,
                address_id=order.address_id,
                payment_method_id=order.payment_method_id,
                total_amount=order.total_amount,
                status=order.status,
                created_at=order.created_at,
                updated_at=order.updated_at,
                items=list(order.items),
                address=order.address,
                payment_method=order.payment_method.type,
            )
            for order in all_orders
        ]

        return BaseResponse(
            message="Orders retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={"orders": orders_response},
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving cart: {str(e)}",
        )
        
        
@router.get("/", response_model=BaseResponse)
async def get_all_orders(
    session: Session = Depends(get_session),
    auth=Depends(get_current_user)
) -> BaseResponse:
    try:
        # Replace with actual user ID retrieval logic
        all_orders = session.exec(select(Order)).all()

        if not all_orders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id '{id}' not found",
            )

        orders_response = [
            OrderResponse(
                id=order.id,
                user_id=order.user_id,
                address_id=order.address_id,
                payment_method_id=order.payment_method_id,
                total_amount=order.total_amount,
                status=order.status,
                created_at=order.created_at,
                updated_at=order.updated_at,
                items=list(order.items),
                address=order.address,
                payment_method=order.payment_method.type,
            )
            for order in all_orders
        ]

        return BaseResponse(
            message="Orders retrieved successfully.",
            status_code=status.HTTP_200_OK,
            detail={"orders": orders_response},
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving cart: {str(e)}",
        )


@router.post("/", response_model=BaseResponse)
async def add_order(
    order_info: OrderCreate, session: Session = Depends(get_session)
) -> BaseResponse:
    try:
        new_order = Order(**order_info.model_dump(exclude={"items"}))

        if not order_info.items or len(order_info.items) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order must contain at least one item.",
            )

        payment_method = session.exec(
            select(PaymentMethod).where(
                PaymentMethod.id == order_info.payment_method_id
            )
        ).first()
        if not payment_method:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment method '{order_info.payment_method_id}' not found",
            )

        user = session.exec(select(User).where(User.id == order_info.user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id '{order_info.user_id}' not found",
            )

        session.add(new_order)

        for item in order_info.items:
            product = session.exec(
                select(Product).where(Product.id == item.product_id)
            ).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id {item.product_id} not found",
                )
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough stock available. Only {product.stock} items left.",
                )
            # Create new order item
            order_item_db = OrderItem(**item.model_dump(), order_id=new_order.id)
            session.add(order_item_db)

        session.add(new_order)
        session.commit()
        session.refresh(new_order)

        for order_item in session.exec(
            select(OrderItem).where(OrderItem.order_id == new_order.id)
        ).all():
            print(f"order_item: {order_item}")

        return BaseResponse(
            message="Order created successfully.",
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=(
                e.status_code
                if hasattr(e, "status_code")
                else status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=f"Error creating order: {str(e.detail) if hasattr(e, 'detail') else str(e)}",
        )
