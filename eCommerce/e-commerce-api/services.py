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
        # Check if username or email already exists
        existing_user = self.db.query(User).filter(
            or_(User.username == user_data.username, User.email == user_data.email)
        ).first()

        if existing_user:
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
        return db_user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()


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
        query = self.db.query(Product).filter(Product.is_active == True)

        if category:
            query = query.filter(Product.category == category)

        if search:
            query = query.filter(
                or_(
                    Product.name.contains(search),
                    Product.description.contains(search)
                )
            )

        return query.offset(skip).limit(limit).all()

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.db.query(Product).filter(
            Product.id == product_id,
            Product.is_active == True
        ).first()

    def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product"""
        db_product = Product(**product_data.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        """Update a product"""
        db_product = self.get_product_by_id(product_id)
        if not db_product:
            return None

        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)

        self.db.commit()
        self.db.refresh(db_product)
        return db_product


class CartService:
    """
    Shopping cart service following Single Responsibility Principle.
    Handles all cart-related business logic.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_cart_items(self, user_id: int) -> List[CartItem]:
        """Get all cart items for a user"""
        return self.db.query(CartItem).filter(CartItem.user_id == user_id).all()

    def add_to_cart(self, user_id: int, cart_item_data: CartItemCreate) -> CartItem:
        """Add item to cart or update quantity if already exists"""
        # Check if product exists
        product = self.db.query(Product).filter(
            Product.id == cart_item_data.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # Check if item already in cart
        existing_item = self.db.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.product_id == cart_item_data.product_id
        ).first()

        if existing_item:
            existing_item.quantity += cart_item_data.quantity
            self.db.commit()
            self.db.refresh(existing_item)
            return existing_item

        # Create new cart item
        db_cart_item = CartItem(
            user_id=user_id,
            product_id=cart_item_data.product_id,
            quantity=cart_item_data.quantity
        )
        self.db.add(db_cart_item)
        self.db.commit()
        self.db.refresh(db_cart_item)
        return db_cart_item

    def update_cart_item(
        self,
        user_id: int,
        cart_item_id: int,
        cart_item_data: CartItemUpdate
    ) -> Optional[CartItem]:
        """Update cart item quantity"""
        db_cart_item = self.db.query(CartItem).filter(
            CartItem.id == cart_item_id,
            CartItem.user_id == user_id
        ).first()

        if not db_cart_item:
            return None

        db_cart_item.quantity = cart_item_data.quantity
        self.db.commit()
        self.db.refresh(db_cart_item)
        return db_cart_item

    def remove_from_cart(self, user_id: int, cart_item_id: int) -> bool:
        """Remove item from cart"""
        db_cart_item = self.db.query(CartItem).filter(
            CartItem.id == cart_item_id,
            CartItem.user_id == user_id
        ).first()

        if not db_cart_item:
            return False

        self.db.delete(db_cart_item)
        self.db.commit()
        return True

    def clear_cart(self, user_id: int) -> None:
        """Clear all items from cart"""
        self.db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        self.db.commit()

    def calculate_cart_total(self, user_id: int) -> float:
        """Calculate total amount for cart"""
        cart_items = self.get_cart_items(user_id)
        total = sum(item.product.price * item.quantity for item in cart_items)
        return round(total, 2)


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
        # Get cart items
        cart_items = self.cart_service.get_cart_items(user_id)

        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )

        # Calculate total
        total_amount = self.cart_service.calculate_cart_total(user_id)

        # Create order
        db_order = Order(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=order_data.shipping_address,
            payment_method=order_data.payment_method,
            status="completed"
        )
        self.db.add(db_order)
        self.db.flush()  # Get order ID without committing

        # Create order items from cart
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=db_order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price_at_purchase=cart_item.product.price
            )
            self.db.add(order_item)

        # Clear cart
        self.cart_service.clear_cart(user_id)

        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def get_user_orders(self, user_id: int) -> List[Order]:
        """Get all orders for a user"""
        return self.db.query(Order).filter(Order.user_id == user_id).all()

    def get_order_by_id(self, user_id: int, order_id: int) -> Optional[Order]:
        """Get specific order for a user"""
        return self.db.query(Order).filter(
            Order.id == order_id,
            Order.user_id == user_id
        ).first()
