from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    """Base user schema following DRY principle"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    """Schema for user response (no password)"""
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


# Token Schemas
class Token(BaseModel):
    """JWT token response schema"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None


# Product Schemas
class ProductBase(BaseModel):
    """Base product schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    image_url: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    inventory_count: int = Field(default=0, ge=0)


class ProductCreate(ProductBase):
    """Schema for creating a product"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    inventory_count: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for product response"""
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# CartItem Schemas
class CartItemBase(BaseModel):
    """Base cart item schema"""
    product_id: int
    quantity: int = Field(..., gt=0)


class CartItemCreate(CartItemBase):
    """Schema for adding item to cart"""
    pass


class CartItemUpdate(BaseModel):
    """Schema for updating cart item"""
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):
    """Schema for cart item response"""
    id: int
    product_id: int
    quantity: int
    added_at: datetime
    product: ProductResponse

    model_config = ConfigDict(from_attributes=True)


# Order Schemas
class OrderItemBase(BaseModel):
    """Base order item schema"""
    product_id: int
    quantity: int = Field(..., gt=0)
    price_at_purchase: float


class OrderItemResponse(OrderItemBase):
    """Schema for order item response"""
    id: int
    product: ProductResponse

    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    """Base order schema"""
    shipping_address: str
    payment_method: str


class OrderCreate(OrderBase):
    """Schema for creating an order"""
    pass


class OrderResponse(OrderBase):
    """Schema for order response"""
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime
    order_items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


# Additional response schemas
class CartSummary(BaseModel):
    """Summary of cart contents"""
    items: List[CartItemResponse]
    total_items: int
    total_amount: float
