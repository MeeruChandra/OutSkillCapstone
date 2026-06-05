# E-Commerce Frontend

A modern React-based e-commerce frontend application built with Vite, featuring a clean UI similar to Swag Labs.

## Features

- User authentication (login/logout)
- Product browsing with search and category filters
- Product detail pages
- Shopping cart management
- Checkout process
- Order history
- Responsive design

## SOLID Principles Implementation

This frontend follows SOLID principles through:

- **Single Responsibility**: Each service class handles one specific domain (AuthService, ProductService, CartService, OrderService)
- **Open/Closed**: React components are open for extension through props but closed for modification
- **Liskov Substitution**: Context providers can be replaced with alternative implementations
- **Interface Segregation**: Services provide focused, specific APIs
- **Dependency Inversion**: Components depend on context abstractions rather than concrete implementations

## Tech Stack

- **React 18** - UI library
- **React Router DOM** - Client-side routing
- **Axios** - HTTP client
- **Vite** - Build tool and dev server
- **Context API** - State management

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

## Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Project Structure

```
e-commerce-frontend/
├── src/
│   ├── components/         # Reusable components
│   │   ├── Header.jsx
│   │   ├── ProductCard.jsx
│   │   └── ProtectedRoute.jsx
│   ├── context/           # React Context providers
│   │   ├── AuthContext.jsx
│   │   └── CartContext.jsx
│   ├── pages/             # Page components
│   │   ├── Login.jsx
│   │   ├── Products.jsx
│   │   ├── ProductDetail.jsx
│   │   ├── Cart.jsx
│   │   ├── Checkout.jsx
│   │   └── Orders.jsx
│   ├── services/          # API service layer
│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── productService.js
│   │   ├── cartService.js
│   │   └── orderService.js
│   ├── App.jsx            # Root component
│   ├── main.jsx           # Entry point
│   └── App.css            # Global styles
├── index.html
├── vite.config.js
└── package.json
```

## Service Layer Architecture

### API Service
- Central axios instance with interceptors
- Automatic JWT token attachment
- Global error handling
- Automatic redirect on 401

### Domain Services
Each service follows SRP and handles specific domain logic:

- **AuthService**: Authentication and user management
- **ProductService**: Product catalog operations
- **CartService**: Shopping cart management
- **OrderService**: Order processing

## Context Providers

### AuthContext
- User authentication state
- Login/logout functionality
- Protected route handling

### CartContext
- Cart state management
- Add/update/remove cart items
- Cart total calculations

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Test Credentials

- **Username**: standard_user
- **Password**: secret_sauce

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000`. Make sure the backend is running before starting the frontend.

API endpoints used:
- `/api/auth/*` - Authentication
- `/api/products/*` - Product catalog
- `/api/cart/*` - Shopping cart
- `/api/orders/*` - Order management

## Features Overview

### Login Page
- User authentication with JWT tokens
- Form validation
- Error handling
- Test credentials display

### Products Page
- Grid layout of products
- Search functionality
- Category filtering
- Add to cart from listing

### Product Detail Page
- Full product information
- Quantity selection
- Add to cart with quantity
- Stock availability

### Shopping Cart
- View cart items
- Update quantities
- Remove items
- Cart total calculation
- Proceed to checkout

### Checkout Page
- Shipping information form
- Payment method selection
- Order summary
- Form validation

### Orders Page
- Order history
- Expandable order details
- Order status
- Order items breakdown

## Responsive Design

The application is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
