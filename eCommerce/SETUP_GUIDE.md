# E-Commerce Application Setup Guide

Complete step-by-step guide to set up and run the e-commerce application.

## Prerequisites

Before starting, ensure you have:

- Python 3.8 or higher installed
- Node.js 16 or higher installed
- npm or yarn package manager
- Git (optional)

## Project Overview

This project consists of two parts:
1. **Backend API** (`e-commerce-api/`) - FastAPI REST API with SQLite
2. **Frontend** (`e-commerce-frontend/`) - React SPA

## Part 1: Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd e-commerce-api
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI
- Uvicorn
- SQLAlchemy
- Python-JOSE (JWT)
- Passlib (password hashing)
- Pydantic

### Step 4: Configure Environment

Create a `.env` file:

```bash
# Copy the example file
cp .env.example .env
```

Or manually create `.env` with:
```
DATABASE_URL=sqlite:///./ecommerce.db
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important**: Change the SECRET_KEY in production!

### Step 5: Seed the Database

```bash
python seed_data.py
```

This will:
- Create all database tables
- Add 6 sample products
- Create 3 test users

Expected output:
```
Creating users...
Creating products...
Database seeded successfully!

==================================================
TEST USER CREDENTIALS
==================================================
Username: standard_user
Password: secret_sauce
--------------------------------------------------
Username: problem_user
Password: secret_sauce
--------------------------------------------------
Username: performance_user
Password: secret_sauce
--------------------------------------------------
```

### Step 6: Run the Backend

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API should now be running at:
- API: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Test the API:**
Visit `http://localhost:8000/docs` to see the interactive API documentation.

### Troubleshooting Backend

**Error: Module not found**
```bash
pip install -r requirements.txt
```

**Error: Port already in use**
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

**Error: Database locked**
- Close any other processes using the database
- Delete `ecommerce.db` and run `python seed_data.py` again

## Part 2: Frontend Setup

Open a **new terminal window** (keep the backend running in the first terminal).

### Step 1: Navigate to Frontend Directory

```bash
cd e-commerce-frontend
```

### Step 2: Install Node Dependencies

```bash
npm install
```

This will install:
- React
- React Router DOM
- Axios
- Vite

**If npm is slow**, you can use yarn:
```bash
yarn install
```

### Step 3: Run the Frontend

```bash
npm run dev
```

The frontend should now be running at:
- `http://localhost:3000`

**Expected output:**
```
  VITE v5.0.8  ready in 523 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

### Troubleshooting Frontend

**Error: Port 3000 already in use**
- Edit `vite.config.js` to change the port
- Or stop the process using port 3000

**Error: Cannot connect to API**
- Make sure backend is running on `http://localhost:8000`
- Check browser console for errors

**Error: CORS issues**
- Backend has CORS configured for `http://localhost:3000`
- If using different port, update CORS settings in `main.py`

## Testing the Application

### 1. Open the Application

Visit `http://localhost:3000` in your browser.

### 2. Login

Use these test credentials:
- **Username**: `standard_user`
- **Password**: `secret_sauce`

### 3. Test Features

1. **Browse Products**
   - View product grid
   - Use search functionality
   - Filter by category

2. **Add to Cart**
   - Click "Add to Cart" on any product
   - View cart badge update in header

3. **View Product Details**
   - Click on a product card
   - Change quantity
   - Add to cart

4. **Shopping Cart**
   - Click "Cart" in header
   - Update quantities (+/- buttons)
   - Remove items
   - See total calculation

5. **Checkout**
   - Click "Proceed to Checkout"
   - Fill shipping information
   - Select payment method
   - Place order

6. **View Orders**
   - Click "Orders" in header
   - Expand order to see details
   - View order items

## API Testing with Swagger

### 1. Open API Documentation
Visit `http://localhost:8000/docs`

### 2. Test Authentication

1. Click on `POST /api/auth/login`
2. Click "Try it out"
3. Enter credentials:
   ```json
   {
     "username": "standard_user",
     "password": "secret_sauce"
   }
   ```
4. Click "Execute"
5. Copy the `access_token` from response

### 3. Authorize API Calls

1. Click "Authorize" button at top
2. Enter: `Bearer <your-token>`
3. Click "Authorize"

Now you can test protected endpoints!

## Common Issues and Solutions

### Backend Issues

**Import Errors**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Database Issues**
```bash
# Reset database
rm ecommerce.db
python seed_data.py
```

**JWT Token Errors**
- Check SECRET_KEY is at least 32 characters
- Ensure ALGORITHM is "HS256"

### Frontend Issues

**Build Errors**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API Connection Issues**
- Check backend is running
- Verify URL in `src/services/api.js`
- Check browser console for errors

**Login Not Working**
- Check credentials
- Check backend logs
- Open browser DevTools Network tab

## Development Tips

### Backend Development

**Hot Reload**
The `--reload` flag automatically restarts the server when code changes.

**View Logs**
All console output shows in the terminal where you ran `python main.py`

**Database Inspection**
Use SQLite browser or:
```bash
sqlite3 ecommerce.db
.tables
SELECT * FROM users;
.quit
```

### Frontend Development

**Hot Reload**
Vite automatically refreshes the browser on code changes.

**View React DevTools**
Install React DevTools browser extension for debugging.

**View Network Requests**
Open browser DevTools → Network tab to see API calls.

## Production Deployment

### Backend

1. Update `.env` with production values
2. Use production ASGI server:
   ```bash
   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```
3. Use PostgreSQL instead of SQLite
4. Enable HTTPS

### Frontend

1. Build production bundle:
   ```bash
   npm run build
   ```
2. Deploy `dist/` folder to hosting service
3. Update API URL to production backend
4. Configure environment variables

## Project Structure

```
OutSkillCapstone/
├── e-commerce-api/          # Backend
│   ├── routers/             # API endpoints
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── services.py          # Business logic
│   ├── auth.py              # Authentication
│   ├── database.py          # DB configuration
│   ├── config.py            # Settings
│   ├── main.py              # App entry point
│   ├── seed_data.py         # Database seeding
│   └── requirements.txt     # Python dependencies
│
├── e-commerce-frontend/     # Frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── context/         # React contexts
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── App.jsx          # Root component
│   │   └── main.jsx         # Entry point
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
└── README.md                # This file
```

## Next Steps

1. Explore the code to understand SOLID principles implementation
2. Try adding new features (e.g., product reviews, wishlist)
3. Customize the UI styling
4. Add more test users and products
5. Implement additional payment methods
6. Add product categories management

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Vite Documentation](https://vitejs.dev/)

## Support

For issues or questions:
1. Check the troubleshooting sections above
2. Review the README files in each project directory
3. Check the API documentation at `/docs`
4. Review browser console and server logs

## License

This is an educational project for learning purposes.
