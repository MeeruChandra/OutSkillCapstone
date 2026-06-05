from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import CartItemResponse, CartItemCreate, CartItemUpdate, CartSummary
from services import CartService
from auth import get_current_active_user
from models import User

router = APIRouter(prefix="/api/cart", tags=["Shopping Cart"])


@router.get("/", response_model=CartSummary)
def get_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's cart"""
    cart_service = CartService(db)
    items = cart_service.get_cart_items(current_user.id)
    total_amount = cart_service.calculate_cart_total(current_user.id)

    return {
        "items": items,
        "total_items": len(items),
        "total_amount": total_amount
    }


@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    cart_item_data: CartItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    cart_service = CartService(db)
    return cart_service.add_to_cart(current_user.id, cart_item_data)


@router.put("/items/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(
    cart_item_id: int,
    cart_item_data: CartItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    cart_service = CartService(db)
    cart_item = cart_service.update_cart_item(
        current_user.id,
        cart_item_id,
        cart_item_data
    )

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )

    return cart_item


@router.delete("/items/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    cart_item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    cart_service = CartService(db)
    success = cart_service.remove_from_cart(current_user.id, cart_item_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Clear all items from cart"""
    cart_service = CartService(db)
    cart_service.clear_cart(current_user.id)
