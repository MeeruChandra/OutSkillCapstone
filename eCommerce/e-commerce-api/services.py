from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from models import User, Product, CartItem, Order, OrderItem
from schemas import (
    UserCreate, ProductCreate, ProductUpdate,
    CartItemCreate, CartItemUpdate, OrderCreate
)
from auth import PasswordHasher
from logger import get_logger

logger = get_logger(__name__)


class UserService:
    """
    User service following Single Responsibility Principle.
    Handles all user-related business logic.
    """

    def __init__(self, db: Session):
        self.db = db
        self.password_hasher = PasswordHasher()

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        logger.info(f"Creating new user: {user_data.username}")
        try:
            existing_user = self.db.query(User).filter(
                or_(User.username == user_data.username, User.email == user_data.email)
            ).first()

            if existing_user:
                logger.warning(
                    f"User creation failed: Username '{user_data.username}' "
                    f"or email '{user_data.email}' already exists"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username or email already registered"
                )

            hashed_password = self.password_hasher.get_password_hash(user_data.password)
            db_user = User(
                username=user_data.username,
                email=user_data.email,
                hashed_password=hashed_password,
                first_name=user_data.first_name,
                last_name=user_data.last_name
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            logger.info(f"User created successfully: {user_data.username} (ID: {db_user.id})")
            return db_user
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating user '{user_data.username}': {str(e)}", exc_info=True)
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        logger.debug(f"Fetching user by ID: {user_id}")
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                logger.debug(f"User found: ID {user_id}")
            else:
                logger.debug(f"User not found: ID {user_id}")
            return user
        except Exception as e:
            logger.error(f"Error fetching user ID {user_id}: {str(e)}", exc_info=True)
            return None


class ProductService:
    """
    Product service following Single Responsibility Principle.
    Handles all product-related business logic.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_products(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Product]:
        """Get list of products with optional filtering"""
        logger.info(f"Fetching products - skip: {skip}, limit: {limit}, category: {category}, search: {search}")
        try:
            query = self.db.query(Product).filter(Product.is_active == True)

            if category:
                query = query.filter(Product.category == category)
                logger.debug(f"Filtering by category: {category}")

            if search:
                query = query.filter(
                    or_(
                        Product.name.contains(search),
                        Product.description.contains(search)
                    )
                )
                logger.debug(f"Filtering by search term: {search}")

            products = query.offset(skip).limit(limit).all()
            logger.info(f"Retrieved {len(products)} products")
            return products
        except Exception as e:
            logger.error(f"Error fetching products: {str(e)}", exc_info=True)
            return []

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        logger.debug(f"Fetching product by ID: {product_id}")
        try:
            product = self.db.query(Product).filter(
                Product.id == product_id,
                Product.is_active == True
            ).first()
            if product:
                logger.debug(f"Product found: {product.name} (ID: {product_id})")
            else:
                logger.warning(f"Product not found or inactive: ID {product_id}")
            return product
        except Exception as e:
            logger.error(f"Error fetching product ID {product_id}: {str(e)}", exc_info=True)
            return None

    def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product"""
        logger.info(f"Creating new product: {product_data.name}")
        try:
            db_product = Product(**product_data.model_dump())
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)
            logger.info(f"Product created successfully: {product_data.name} (ID: {db_product.id})")
            return db_product
        except Exception as e:
            logger.error(f"Error creating product '{product_data.name}': {str(e)}", exc_info=True)
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create product"
            )

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        """Update a product"""
        logger.info(f"Updating product ID: {product_id}")
        try:
            db_product = self.get_product_by_id(product_id)
            if not db_product:
                logger.warning(f"Cannot update - product not found: ID {product_id}")
                return None

            update_data = product_data.model_dump(exclude_unset=True)
            logger.debug(f"Update fields: {list(update_data.keys())}")
            for field, value in update_data.items():
                setattr(db_product, field, value)

            self.db.commit()
            self.db.refresh(db_product)
            logger.info(f"Product updated successfully: {db_product.name} (ID: {product_id})")
            return db_product
        except Exception as e:
            logger.error(f"Error updating product ID {product_id}: {str(e)}", exc_info=True)
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update product"
            )


class CartService:
    """
    Shopping cart service following Single Responsibility Principle.
    Handles all cart-related business logic.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_cart_items(self, user_id: int) -> List[CartItem]:
        """Get all cart items for a user"""
        logger.debug(f"Fetching cart items for user ID: {user_id}")
        try:
            items = self.db.query(CartItem).filter(CartItem.user_id == user_id).all()
            logger.info(f"Retrieved {len(items)} cart items for user ID: {user_id}")
            return items
        except Exception as e:
            logger.error(f"Error fetching cart items for user ID {user_id}: {str(e)}", exc_info=True)
            return []

    def add_to_cart(self, user_id: int, cart_item_data: CartItemCreate) -> CartItem:
        """Add item to cart or update quantity if already exists"""
        logger.info(f"Adding product ID {cart_item_data.product_id} to cart for user ID {user_id}")
        try:
            product = self.db.query(Product).filter(
                Product.id == cart_item_data.product_id
            ).first()

            if not product:
                logger.warning(f"Cannot add to cart - product not found: ID {cart_item_data.product_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )

            existing_item = self.db.query(CartItem).filter(
                CartItem.user_id == user_id,
                CartItem.product_id == cart_item_data.product_id
            ).first()

            if existing_item:
                logger.debug(f"Product already in cart, updating quantity from {existing_item.quantity} to {existing_item.quantity + cart_item_data.quantity}")
                existing_item.quantity += cart_item_data.quantity
                self.db.commit()
                self.db.refresh(existing_item)
                logger.info(f"Cart item updated: Product ID {cart_item_data.product_id}, new quantity: {existing_item.quantity}")
                return existing_item

            db_cart_item = CartItem(
                user_id=user_id,
                product_id=cart_item_data.product_id,
                quantity=cart_item_data.quantity
            )
            self.db.add(db_cart_item)
            self.db.commit()
            self.db.refresh(db_cart_item)
            logger.info(f"Cart item added: Product ID {cart_item_data.product_id}, quantity: {cart_item_data.quantity}")
            return db_cart_item
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error adding product ID {cart_item_data.product_id} to cart: {str(e)}", exc_info=True)
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add item to cart"
            )

    def update_cart_item(
        self,
        user_id: int,
        cart_item_id: int,
        cart_item_data: CartItemUpdate
    ) -> Optional[CartItem]:
        """Update cart item quantity"""
        logger.info(f"Updating cart item ID {cart_item_id} for user ID {user_id}")
        try:
            db_cart_item = self.db.query(CartItem).filter(
                CartItem.id == cart_item_id,
                CartItem.user_id == user_id
            ).first()

            if not db_cart_item:
                logger.warning(f"Cart item not found: ID {cart_item_id} for user ID {user_id}")
                return None

            old_quantity = db_cart_item.quantity
            db_cart_item.quantity = cart_item_data.quantity
            self.db.commit()
            self.db.refresh(db_cart_item)
            logger.info(f"Cart item ID {cart_item_id} updated: quantity {old_quantity} -> {cart_item_data.quantity}")
            return db_cart_item
        except Exception as e:
            logger.error(f"Error updating cart item ID {cart_item_id}: {str(e)}", exc_info=True)
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update cart item"
            )

    def remove_from_cart(self, user_id: int, cart_item_id: int) -> bool:
        """Remove item from cart"""
        logger.info(f"Removing cart item ID {cart_item_id} for user ID {user_id}")
        try:
            db_cart_item = self.db.query(CartItem).filter(
                CartItem.id == cart_item_id,
                CartItem.user_id == user_id
            ).first()

            if not db_cart_item:
                logger.warning(f"Cannot remove - cart item not found: ID {cart_item_id} for user ID {user_id}")
                return False

            self.db.delete(db_cart_item)
            self.db.commit()
            logger.info(f"Cart item ID {cart_item_id} removed successfully")
            return True
        except Exception as e:
            logger.error(f"Error removing cart item ID {cart_item_id}: {str(e)}", exc_info=True)
            self.db.rollback()
            return False

    def clear_cart(self, user_id: int) -> None:
        """Clear all items from cart"""
        logger.info(f"Clearing cart for user ID {user_id}")
        try:
            deleted_count = self.db.query(CartItem).filter(CartItem.user_id == user_id).delete()
            self.db.commit()
            logger.info(f"Cart cleared: {deleted_count} items removed for user ID {user_id}")
        except Exception as e:
            logger.error(f"Error clearing cart for user ID {user_id}: {str(e)}", exc_info=True)
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to clear cart"
            )

    def calculate_cart_total(self, user_id: int) -> float:
        """Calculate total amount for cart"""
        logger.debug(f"Calculating cart total for user ID {user_id}")
        try:
            cart_items = self.get_cart_items(user_id)
            total = sum(item.product.price * item.quantity for item in cart_items)
            total = round(total, 2)
            logger.debug(f"Cart total for user ID {user_id}: ${total}")
            return total
        except Exception as e:
            logger.error(f"Error calculating cart total for user ID {user_id}: {str(e)}", exc_info=True)
            return 0.0


class OrderService:
    """
    Order service following Single Responsibility Principle.
    Handles all order-related business logic.
    """

    def __init__(self, db: Session):
        self.db = db
        self.cart_service = CartService(db)

    def create_order(self, user_id: int, order_data: OrderCreate) -> Order:
        """Create order from cart items"""
        logger.info(f"Creating order for user ID {user_id}")
        try:
            cart_items = self.cart_service.get_cart_items(user_id)

            if not cart_items:
                logger.warning(f"Cannot create order - cart is empty for user ID {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cart is empty"
                )

            logger.debug(f"Processing {len(cart_items)} cart items for order")
            total_amount = self.cart_service.calculate_cart_total(user_id)
            logger.debug(f"Order total amount: ${total_amount}")

            db_order = Order(
                user_id=user_id,
                total_amount=total_amount,
                shipping_address=order_data.shipping_address,
                payment_method=order_data.payment_method,
                status="completed"
            )
            self.db.add(db_order)
            self.db.flush()
            logger.debug(f"Order created with ID: {db_order.id}")

            for cart_item in cart_items:
                order_item = OrderItem(
                    order_id=db_order.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price_at_purchase=cart_item.product.price
                )
                self.db.add(order_item)
                logger.debug(f"Order item added: Product ID {cart_item.product_id}, quantity: {cart_item.quantity}")

            self.cart_service.clear_cart(user_id)
            logger.debug("Cart cleared after order creation")

            self.db.commit()
            self.db.refresh(db_order)
            logger.info(f"Order created successfully: Order ID {db_order.id}, Total: ${total_amount}")
            return db_order
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating order for user ID {user_id}: {str(e)}", exc_info=True)
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create order"
            )

    def get_user_orders(self, user_id: int) -> List[Order]:
        """Get all orders for a user"""
        logger.debug(f"Fetching orders for user ID {user_id}")
        try:
            orders = self.db.query(Order).filter(Order.user_id == user_id).all()
            logger.info(f"Retrieved {len(orders)} orders for user ID {user_id}")
            return orders
        except Exception as e:
            logger.error(f"Error fetching orders for user ID {user_id}: {str(e)}", exc_info=True)
            return []

    def get_order_by_id(self, user_id: int, order_id: int) -> Optional[Order]:
        """Get specific order for a user"""
        logger.debug(f"Fetching order ID {order_id} for user ID {user_id}")
        try:
            order = self.db.query(Order).filter(
                Order.id == order_id,
                Order.user_id == user_id
            ).first()
            if order:
                logger.debug(f"Order found: ID {order_id}")
            else:
                logger.warning(f"Order not found: ID {order_id} for user ID {user_id}")
            return order
        except Exception as e:
            logger.error(f"Error fetching order ID {order_id}: {str(e)}", exc_info=True)
            return None
