# E-Commerce API

A RESTful API for an e-commerce application built with FastAPI, SQLAlchemy, and SQLite.

## Features

- User authentication with JWT tokens
- Product catalog management
- Shopping cart functionality
- Order processing
- CORS enabled for frontend integration

## SOLID Principles Implementation

This project follows SOLID principles:

- **Single Responsibility**: Each service class handles one specific domain (UserService, ProductService, CartService, OrderService)
- **Open/Closed**: Services are open for extension but closed for modification
- **Liskov Substitution**: Database session dependency injection allows for easy testing with mock databases
- **Interface Segregation**: Separate routers for different API domains
- **Dependency Inversion**: Services depend on abstractions (Session) rather than concrete implementations

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Seed the database with initial data:
```bash
python seed_data.py
```

6. Run the application:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Test Credentials

After seeding the database, use these credentials:

- **Username**: standard_user
- **Password**: secret_sauce

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Products
- `GET /api/products` - Get all products (with optional filtering)
- `GET /api/products/{id}` - Get product by ID
- `POST /api/products` - Create new product
- `PUT /api/products/{id}` - Update product

### Cart
- `GET /api/cart` - Get cart summary
- `POST /api/cart/items` - Add item to cart
- `PUT /api/cart/items/{id}` - Update cart item quantity
- `DELETE /api/cart/items/{id}` - Remove item from cart
- `DELETE /api/cart` - Clear cart

### Orders
- `POST /api/orders` - Create order from cart
- `GET /api/orders` - Get user's orders
- `GET /api/orders/{id}` - Get specific order

## Project Structure

```
e-commerce-api/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration settings
├── database.py          # Database connection and session
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication services
├── services.py          # Business logic services
├── seed_data.py         # Database seeding script
├── routers/             # API route handlers
│   ├── auth_router.py
│   ├── products_router.py
│   ├── cart_router.py
│   └── orders_router.py
└── requirements.txt     # Python dependencies
```

## Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **Uvicorn**: ASGI server
