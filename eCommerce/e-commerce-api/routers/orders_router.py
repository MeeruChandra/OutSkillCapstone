from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import OrderResponse, OrderCreate
from services import OrderService
from auth import get_current_active_user
from models import User

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create order from cart items"""
    order_service = OrderService(db)
    return order_service.create_order(current_user.id, order_data)


@router.get("/", response_model=List[OrderResponse])
def get_orders(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all orders for current user"""
    order_service = OrderService(db)
    return order_service.get_user_orders(current_user.id)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific order by ID"""
    order_service = OrderService(db)
    order = order_service.get_order_by_id(current_user.id, order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order
