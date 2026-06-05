from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import OrderResponse, OrderCreate
from services import OrderService
from auth import get_current_active_user
from models import User
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create order from cart items"""
    logger.info(f"Create order request for user: {current_user.username}")
    try:
        order_service = OrderService(db)
        order = order_service.create_order(current_user.id, order_data)
        logger.info(f"Order created successfully for user {current_user.username}: Order ID {order.id}")
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order for user {current_user.username}: {str(e)}", exc_info=True)
        raise


@router.get("/", response_model=List[OrderResponse])
def get_orders(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all orders for current user"""
    logger.info(f"Get orders request for user: {current_user.username}")
    try:
        order_service = OrderService(db)
        orders = order_service.get_user_orders(current_user.id)
        logger.info(f"Retrieved {len(orders)} orders for user: {current_user.username}")
        return orders
    except Exception as e:
        logger.error(f"Error fetching orders for user {current_user.username}: {str(e)}", exc_info=True)
        raise


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific order by ID"""
    logger.info(f"Get order detail request for user {current_user.username}: Order ID {order_id}")
    try:
        order_service = OrderService(db)
        order = order_service.get_order_by_id(current_user.id, order_id)

        if not order:
            logger.warning(f"Order not found: ID {order_id} for user {current_user.username}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        logger.info(f"Order retrieved for user {current_user.username}: Order ID {order_id}")
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching order {order_id} for user {current_user.username}: {str(e)}", exc_info=True)
        raise
