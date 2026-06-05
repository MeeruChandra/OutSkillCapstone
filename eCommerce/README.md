# E-Commerce Application

A full-stack e-commerce application inspired by Swag Labs, built with FastAPI (Python) backend and React frontend.

## Project Structure

This repository contains two separate projects:

### `/e-commerce-api` - Backend API
FastAPI-based REST API with SQLite database

### `/e-commerce-frontend` - Frontend Application
React-based single-page application with Vite

## Features

- **User Authentication**: JWT-based authentication system
- **Product Catalog**: Browse products with search and filtering
- **Shopping Cart**: Add, update, and remove items
- **Checkout Process**: Complete order with shipping information
- **Order Management**: View order history and details
- **Responsive Design**: Mobile-friendly interface

## SOLID Principles

Both projects follow SOLID principles:

### Backend (Python/FastAPI)
- **Single Responsibility**: Separate service classes for User, Product, Cart, and Order domains
- **Open/Closed**: Services are extensible without modification
- **Liskov Substitution**: Database session dependency injection allows testing with mocks
- **Interface Segregation**: Separate routers for different API domains
- **Dependency Inversion**: Services depend on Session abstraction

### Frontend (React)
- **Single Responsibility**: Each service handles one domain (Auth, Product, Cart, Order)
- **Open/Closed**: Components use props for extension
- **Liskov Substitution**: Context providers are replaceable
- **Interface Segregation**: Focused service APIs
- **Dependency Inversion**: Components depend on context abstractions

## Tech Stack

### Backend
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database operations
- SQLite - Lightweight database
- JWT - Authentication tokens
- Pydantic - Data validation

### Frontend
- React 18 - UI library
- React Router - Client-side routing
- Axios - HTTP client
- Vite - Build tool
- Context API - State management

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd e-commerce-api
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create `.env` file:
```bash
cp .env.example .env
```

6. Seed database:
```bash
python seed_data.py
```

7. Run the API:
```bash
python main.py
```

Backend will run at `http://localhost:8000`
API docs available at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd e-commerce-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will run at `http://localhost:3000`

## Test Credentials

After seeding the database, use these credentials:

- **Username**: `standard_user`
- **Password**: `secret_sauce`

Additional test users:
- `problem_user` / `secret_sauce`
- `performance_user` / `secret_sauce`

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login with credentials
- `GET /api/auth/me` - Get current user

### Products
- `GET /api/products` - List products (with filters)
- `GET /api/products/{id}` - Get product details
- `POST /api/products` - Create product (admin)
- `PUT /api/products/{id}` - Update product (admin)

### Shopping Cart
- `GET /api/cart` - Get cart summary
- `POST /api/cart/items` - Add item to cart
- `PUT /api/cart/items/{id}` - Update cart item
- `DELETE /api/cart/items/{id}` - Remove from cart
- `DELETE /api/cart` - Clear cart

### Orders
- `POST /api/orders` - Create order from cart
- `GET /api/orders` - Get user orders
- `GET /api/orders/{id}` - Get order details

## Database Schema

### Users
- id, username, email, hashed_password
- first_name, last_name, is_active
- created_at

### Products
- id, name, description, price
- image_url, category, inventory_count
- is_active, created_at

### Cart Items
- id, user_id, product_id
- quantity, added_at

### Orders
- id, user_id, total_amount
- status, shipping_address, payment_method
- created_at, updated_at

### Order Items
- id, order_id, product_id
- quantity, price_at_purchase

## Development

### Backend Development
```bash
cd e-commerce-api
uvicorn main:app --reload
```

### Frontend Development
```bash
cd e-commerce-frontend
npm run dev
```

## Building for Production

### Backend
The FastAPI application can be deployed using:
- Docker
- Gunicorn with Uvicorn workers
- Platform-specific deployment (Heroku, AWS, etc.)

### Frontend
```bash
cd e-commerce-frontend
npm run build
```

The production build will be in the `dist/` directory.

## Architecture Highlights

### Separation of Concerns
- **Backend**: Models, Schemas, Services, Routers are clearly separated
- **Frontend**: Services, Context, Components, Pages have distinct responsibilities

### Service Layer Pattern
Both backend and frontend use service layers to encapsulate business logic and API calls.

### Dependency Injection
- Backend uses FastAPI's dependency injection for database sessions
- Frontend uses React Context for state management

### Authentication Flow
1. User logs in with credentials
2. Backend validates and returns JWT token
3. Frontend stores token in localStorage
4. Token is automatically attached to all API requests
5. Protected routes check authentication status

## License

This project is for educational purposes.

## Contributing

This is a capstone project. For issues or suggestions, please create an issue in the repository.
