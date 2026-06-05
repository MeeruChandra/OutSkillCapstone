# Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User's Browser                          │
│                     http://localhost:3000                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS Requests
                             │ (with JWT Token)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    React Frontend (Vite)                        │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                     Presentation Layer                     │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │ │
│  │  │  Login   │  │ Products │  │   Cart   │  │  Orders  │  │ │
│  │  │   Page   │  │   Page   │  │   Page   │  │   Page   │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │ │
│  │  ┌──────────┐  ┌──────────┐                               │ │
│  │  │ Product  │  │ Checkout │                               │ │
│  │  │  Detail  │  │   Page   │                               │ │
│  │  └──────────┘  └──────────┘                               │ │
│  └─────────────────────────┬─────────────────────────────────┘ │
│                            │                                    │
│  ┌─────────────────────────┴─────────────────────────────────┐ │
│  │                  State Management Layer                    │ │
│  │  ┌─────────────────┐        ┌─────────────────┐          │ │
│  │  │  AuthContext    │        │   CartContext   │          │ │
│  │  │  - user state   │        │   - cart state  │          │ │
│  │  │  - login/logout │        │   - cart ops    │          │ │
│  │  └─────────────────┘        └─────────────────┘          │ │
│  └─────────────────────────┬─────────────────────────────────┘ │
│                            │                                    │
│  ┌─────────────────────────┴─────────────────────────────────┐ │
│  │                    Service Layer (API)                     │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │ │
│  │  │ authService  │  │productService│  │ cartService  │   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │ │
│  │  ┌──────────────┐                                         │ │
│  │  │orderService  │                                         │ │
│  │  └──────────────┘                                         │ │
│  │         │                                                  │ │
│  │         └─────────► Axios HTTP Client ◄──────────────────┤ │
│  │                     (with interceptors)                   │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ REST API Calls
                             │ JSON + JWT
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 FastAPI Backend (Uvicorn)                       │
│                   http://localhost:8000                         │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                      Router Layer                          │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │ │
│  │  │   Auth   │  │ Products │  │   Cart   │  │  Orders  │  │ │
│  │  │  Router  │  │  Router  │  │  Router  │  │  Router  │  │ │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │ │
│  └───────┼─────────────┼─────────────┼─────────────┼────────┘ │
│          │             │             │             │           │
│  ┌───────┴─────────────┴─────────────┴─────────────┴────────┐ │
│  │                    Service Layer                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │ │
│  │  │ UserService  │  │ProductService│  │ CartService  │   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │ │
│  │  ┌──────────────┐  ┌──────────────┐                     │ │
│  │  │OrderService  │  │ AuthService  │                     │ │
│  │  └──────────────┘  └──────────────┘                     │ │
│  └─────────────────────────┬─────────────────────────────────┘ │
│                            │                                    │
│  ┌─────────────────────────┴─────────────────────────────────┐ │
│  │                      Data Layer                            │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │             SQLAlchemy ORM Models                    │ │ │
│  │  │  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐        │ │ │
│  │  │  │ User  │  │Product│  │ Cart  │  │ Order │        │ │ │
│  │  │  └───────┘  └───────┘  └───────┘  └───────┘        │ │ │
│  │  │  ┌───────────┐  ┌───────────┐                       │ │ │
│  │  │  │ CartItem  │  │OrderItem  │                       │ │ │
│  │  │  └───────────┘  └───────────┘                       │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────┬─────────────────────────────────┘ │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  SQLite Database │
                    │  ecommerce.db    │
                    └─────────────────┘
```

## Component Interaction Flow

### 1. User Authentication Flow

```
User enters credentials
         │
         ▼
   Login Page
         │
         ▼
   AuthContext.login()
         │
         ▼
   authService.login()
         │
         ▼
   POST /api/auth/login
         │
         ▼
   AuthRouter.login()
         │
         ▼
   AuthService.authenticate_user()
         │
         ▼
   Database Query (User)
         │
         ▼
   TokenService.create_access_token()
         │
         ▼
   Return JWT Token
         │
         ▼
   Store token in localStorage
         │
         ▼
   Redirect to Products Page
```

### 2. Product Browsing Flow

```
User visits Products Page
         │
         ▼
   Products Component
         │
         ▼
   productService.getProducts()
         │
         ▼
   GET /api/products
         │
         ▼
   ProductsRouter.get_products()
         │
         ▼
   ProductService.get_products()
         │
         ▼
   Database Query (Products)
         │
         ▼
   Return Product List
         │
         ▼
   Display in ProductCard Components
```

### 3. Add to Cart Flow

```
User clicks "Add to Cart"
         │
         ▼
   ProductCard Component
         │
         ▼
   CartContext.addToCart()
         │
         ▼
   cartService.addToCart()
         │
         ▼
   POST /api/cart/items
         │
    (JWT Token sent in header)
         │
         ▼
   get_current_active_user() Dependency
         │
         ▼
   CartRouter.add_to_cart()
         │
         ▼
   CartService.add_to_cart()
         │
         ▼
   Database Insert (CartItem)
         │
         ▼
   Return Updated Cart Item
         │
         ▼
   CartContext.fetchCart()
         │
         ▼
   Update Cart Badge in Header
```

### 4. Checkout Flow

```
User clicks "Proceed to Checkout"
         │
         ▼
   Navigate to Checkout Page
         │
         ▼
   User fills shipping form
         │
         ▼
   User submits order
         │
         ▼
   orderService.createOrder()
         │
         ▼
   POST /api/orders
         │
    (JWT Token sent in header)
         │
         ▼
   get_current_active_user() Dependency
         │
         ▼
   OrdersRouter.create_order()
         │
         ▼
   OrderService.create_order()
         │
         ├─► Get cart items
         │
         ├─► Calculate total
         │
         ├─► Create order record
         │
         ├─► Create order items
         │
         └─► Clear cart
         │
         ▼
   Return Order Details
         │
         ▼
   CartContext.clearCart()
         │
         ▼
   Navigate to Orders Page
```

## Database Schema Relationships

```
┌─────────────┐
│    User     │
│─────────────│
│ id (PK)     │◄──────┐
│ username    │       │
│ email       │       │
│ password    │       │
└─────────────┘       │
                      │ user_id (FK)
┌─────────────┐       │
│  CartItem   │───────┤
│─────────────│       │
│ id (PK)     │       │
│ user_id (FK)├───────┘
│ product_id  ├───────┐
│ quantity    │       │
└─────────────┘       │
                      │ product_id (FK)
┌─────────────┐       │
│   Product   │◄──────┤
│─────────────│       │
│ id (PK)     │       │
│ name        │       │
│ price       │       │
│ category    │       │
│ inventory   │       │
└─────────────┘       │
       ▲              │
       │              │
       │ product_id   │
       │              │
┌─────────────┐       │
│  OrderItem  │───────┘
│─────────────│
│ id (PK)     │
│ order_id    ├───────┐
│ product_id  │       │
│ quantity    │       │
│ price       │       │
└─────────────┘       │ order_id (FK)
                      │
┌─────────────┐       │
│    Order    │◄──────┘
│─────────────│
│ id (PK)     │
│ user_id (FK)├───────┐
│ total       │       │
│ status      │       │ user_id (FK)
│ address     │       │
└─────────────┘       │
       ▲              │
       └──────────────┘
```

## SOLID Principles in Action

### Single Responsibility Principle

```
Backend Services:
┌──────────────────┐
│   UserService    │ → Only manages users
├──────────────────┤
│   ProductService │ → Only manages products
├──────────────────┤
│   CartService    │ → Only manages cart
├──────────────────┤
│   OrderService   │ → Only manages orders
├──────────────────┤
│   AuthService    │ → Only handles authentication
├──────────────────┤
│   TokenService   │ → Only handles JWT tokens
├──────────────────┤
│  PasswordHasher  │ → Only hashes passwords
└──────────────────┘

Frontend Services:
┌──────────────────┐
│   authService    │ → Only auth API calls
├──────────────────┤
│  productService  │ → Only product API calls
├──────────────────┤
│   cartService    │ → Only cart API calls
├──────────────────┤
│   orderService   │ → Only order API calls
└──────────────────┘
```

### Dependency Inversion Principle

```
High-level modules depend on abstractions:

Backend:
┌──────────────┐
│  UserService │
└──────┬───────┘
       │ depends on
       ▼
┌──────────────┐
│   Session    │ ← Abstraction (SQLAlchemy Session)
│ (Interface)  │
└──────────────┘
       ▲
       │ implements
       │
┌──────────────┐
│ SessionLocal │ ← Concrete implementation
└──────────────┘

Frontend:
┌──────────────┐
│   Products   │
│   Component  │
└──────┬───────┘
       │ depends on
       ▼
┌──────────────┐
│ CartContext  │ ← Abstraction (Context API)
│ (Interface)  │
└──────────────┘
       ▲
       │ implements
       │
┌──────────────┐
│ CartProvider │ ← Concrete implementation
└──────────────┘
```

## Security Architecture

### JWT Authentication Flow

```
1. User Login
   ┌──────────┐
   │  Client  │
   └────┬─────┘
        │ POST /api/auth/login
        │ {username, password}
        ▼
   ┌──────────┐
   │  Backend │
   └────┬─────┘
        │ Verify credentials
        │ Generate JWT token
        ▼
   ┌──────────┐
   │  Client  │ Store token in localStorage
   └──────────┘

2. Protected API Calls
   ┌──────────┐
   │  Client  │
   └────┬─────┘
        │ GET /api/cart
        │ Header: Authorization: Bearer <token>
        ▼
   ┌──────────┐
   │  Backend │
   └────┬─────┘
        │ Verify token signature
        │ Extract user from token
        │ Execute request
        ▼
   ┌──────────┐
   │  Client  │ Receive response
   └──────────┘

3. Token Expiry
   ┌──────────┐
   │  Backend │ Returns 401 Unauthorized
   └────┬─────┘
        ▼
   ┌──────────┐
   │  Client  │
   └────┬─────┘
        │ Axios interceptor catches 401
        │ Clears token
        │ Redirects to login
        ▼
   ┌──────────┐
   │  Login   │
   │   Page   │
   └──────────┘
```

## API Documentation

FastAPI automatically generates API documentation:

- **Swagger UI**: Interactive API testing interface
- **ReDoc**: Clean API reference documentation

Both are generated from:
- Route definitions
- Pydantic schemas
- Docstrings
- Type hints

## Error Handling Strategy

```
Frontend Error Handling:
┌─────────────┐
│   Service   │
│   Layer     │ ← try/catch blocks
└──────┬──────┘
       │ throws error
       ▼
┌─────────────┐
│  Component  │ ← catches error
└──────┬──────┘   sets error state
       │           displays to user
       ▼
┌─────────────┐
│  Error UI   │
└─────────────┘

Backend Error Handling:
┌─────────────┐
│   Router    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Service   │ ← Validates input
└──────┬──────┘   Business logic checks
       │           Raises HTTPException
       ▼
┌─────────────┐
│  FastAPI    │ ← Catches exception
└──────┬──────┘   Formats error response
       │           Returns HTTP status code
       ▼
┌─────────────┐
│   Client    │ ← Receives error
└─────────────┘   Displays message
```

## Technology Stack Summary

### Backend Stack
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Development database
- **Pydantic**: Data validation
- **python-jose**: JWT token handling
- **passlib**: Password hashing

### Frontend Stack
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Context API**: State management

### Development Tools
- **Swagger/OpenAPI**: API documentation
- **ReDoc**: Alternative API documentation
- **Hot Reload**: Both backend and frontend
- **Browser DevTools**: Frontend debugging
- **Python Debugger**: Backend debugging

## Deployment Architecture (Future)

```
                    ┌─────────────┐
                    │   Users     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │     CDN     │ (Static Assets)
                    └──────┬──────┘
                           │
                           ▼
┌──────────────────────────────────────────────┐
│            Load Balancer                     │
└──────┬───────────────────────┬───────────────┘
       │                       │
       ▼                       ▼
┌─────────────┐         ┌─────────────┐
│  Frontend   │         │  Frontend   │
│  Server 1   │         │  Server 2   │
└──────┬──────┘         └──────┬──────┘
       │                       │
       └───────────┬───────────┘
                   │
                   ▼
            ┌─────────────┐
            │ API Gateway │
            └──────┬──────┘
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│  Backend   │ │  Backend   │ │  Backend   │
│  Server 1  │ │  Server 2  │ │  Server 3  │
└─────┬──────┘ └─────┬──────┘ └─────┬──────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
           ┌─────────┼─────────┐
           ▼                   ▼
    ┌────────────┐      ┌────────────┐
    │ PostgreSQL │      │   Redis    │
    │  Database  │      │   Cache    │
    └────────────┘      └────────────┘
```

This architecture demonstrates a scalable, maintainable, and secure full-stack e-commerce application following modern best practices and SOLID principles.
