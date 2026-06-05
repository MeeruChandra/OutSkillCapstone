# Quick Start Guide

Get the e-commerce application running in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 16+
- Terminal/Command Prompt

## Step 1: Start Backend (2 minutes)

Open terminal #1:

```bash
# Navigate to backend
cd e-commerce-api

# Create virtual environment (one-time setup)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies (one-time setup)
pip install -r requirements.txt

# Create .env file (one-time setup)
# Windows:
copy .env.example .env
# Mac/Linux:
cp .env.example .env

# Seed database (one-time setup)
python seed_data.py

# Start the backend
python main.py
```

✅ Backend running at: http://localhost:8000
📚 API Docs at: http://localhost:8000/docs

## Step 2: Start Frontend (2 minutes)

Open terminal #2 (keep backend running):

```bash
# Navigate to frontend
cd e-commerce-frontend

# Install dependencies (one-time setup)
npm install

# Start the frontend
npm run dev
```

✅ Frontend running at: http://localhost:3000

## Step 3: Login & Test (1 minute)

1. Open browser: http://localhost:3000
2. Login with:
   - **Username**: `standard_user`
   - **Password**: `secret_sauce`
3. Browse products and add to cart!

## That's It!

You now have a fully functional e-commerce application running locally.

## Next Steps

- 📖 Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
- 📄 Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture details
- 🔧 Explore the code and customize it
- 🚀 Add new features

## Troubleshooting

**Backend won't start?**
- Check if Python is installed: `python --version`
- Make sure virtual environment is activated (you should see `(venv)` in prompt)

**Frontend won't start?**
- Check if Node.js is installed: `node --version`
- Try deleting `node_modules` and running `npm install` again

**Can't login?**
- Make sure backend is running
- Check you ran `python seed_data.py`
- Use exact credentials: `standard_user` / `secret_sauce`

## Available Test Users

| Username | Password |
|----------|----------|
| standard_user | secret_sauce |
| problem_user | secret_sauce |
| performance_user | secret_sauce |

## Project URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |

## Quick Commands Reference

### Backend Commands
```bash
# Activate environment
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Run server
python main.py

# Reset database
rm ecommerce.db && python seed_data.py    # Mac/Linux
del ecommerce.db && python seed_data.py   # Windows
```

### Frontend Commands
```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build
```

## Features to Try

1. **Search Products** - Use the search bar on products page
2. **Filter by Category** - Click category buttons (Clothing, Backpacks, Accessories)
3. **Add to Cart** - Click "Add to Cart" on any product
4. **View Product Details** - Click on a product card
5. **Manage Cart** - Update quantities, remove items
6. **Checkout** - Fill shipping info and place order
7. **View Orders** - See your order history

## Need Help?

- 📖 Read the detailed [SETUP_GUIDE.md](SETUP_GUIDE.md)
- 🔍 Check the [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- 📚 Review API docs at http://localhost:8000/docs
- 🐛 Check browser console and terminal logs for errors

Happy coding! 🚀
