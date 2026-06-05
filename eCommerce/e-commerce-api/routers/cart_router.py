from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import CartItemResponse, CartItemCreate, CartItemUpdate, CartSummary
from services import CartService
from auth import get_current_active_user
from models import User
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/cart", tags=["Shopping Cart"])


@router.get("/", response_model=CartSummary)
def get_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's cart"""
    logger.info(f"Get cart request for user: {current_user.username}")
    try:
        cart_service = CartService(db)
        items = cart_service.get_cart_items(current_user.id)
        total_amount = cart_service.calculate_cart_total(current_user.id)

        logger.info(f"Cart retrieved for {current_user.username}: {len(items)} items, total: ${total_amount}")
        return {
            "items": items,
            "total_items": len(items),
            "total_amount": total_amount
        }
    except Exception as e:
        logger.error(f"Error fetching cart for user {current_user.username}: {str(e)}", exc_info=True)
        raise


@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    cart_item_data: CartItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    logger.info(f"Add to cart request for user {current_user.username}: Product ID {cart_item_data.product_id}")
    try:
        cart_service = CartService(db)
        cart_item = cart_service.add_to_cart(current_user.id, cart_item_data)
        logger.info(f"Item added to cart for user {current_user.username}")
        return cart_item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding to cart for user {current_user.username}: {str(e)}", exc_info=True)
        raise


@router.put("/items/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(
    cart_item_id: int,
    cart_item_data: CartItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    logger.info(f"Update cart item request for user {current_user.username}: Item ID {cart_item_id}")
    try:
        cart_service = CartService(db)
        cart_item = cart_service.update_cart_item(
            current_user.id,
            cart_item_id,
            cart_item_data
        )

        if not cart_item:
            logger.warning(f"Cart item not found: ID {cart_item_id} for user {current_user.username}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )

        logger.info(f"Cart item updated for user {current_user.username}: Item ID {cart_item_id}")
        return cart_item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating cart item for user {current_user.username}: {str(e)}", exc_info=True)
        raise


@router.delete("/items/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    cart_item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    logger.info(f"Remove from cart request for user {current_user.username}: Item ID {cart_item_id}")
    try:
        cart_service = CartService(db)
        success = cart_service.remove_from_cart(current_user.id, cart_item_id)

        if not success:
            logger.warning(f"Cart item not found for removal: ID {cart_item_id} for user {current_user.username}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )

        logger.info(f"Item removed from cart for user {current_user.username}: Item ID {cart_item_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing from cart for user {current_user.username}: {str(e)}", exc_info=True)
        raise


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Clear all items from cart"""
    logger.info(f"Clear cart request for user: {current_user.username}")
    try:
        cart_service = CartService(db)
        cart_service.clear_cart(current_user.id)
        logger.info(f"Cart cleared for user: {current_user.username}")
    except Exception as e:
        logger.error(f"Error clearing cart for user {current_user.username}: {str(e)}", exc_info=True)
        raise
