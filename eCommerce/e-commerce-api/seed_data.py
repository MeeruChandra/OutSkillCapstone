from database import SessionLocal, engine, Base
from models import User, Product
from pwdlib import PasswordHash
# Place this at the very top of seed_data.py
 

# Your existing imports continue below...
# Sample product data similar to saucedemo.com
PRODUCTS_DATA = [
    {
        "name": "Sauce Labs Backpack",
        "description": "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.",
        "price": 29.99,
        "category": "backpacks",
        "inventory_count": 50,
        "image_url": "sauce-backpack-1200x1500.0a0b85a3.jpg"
    },
    {
        "name": "Sauce Labs Bike Light",
        "description": "A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.",
        "price": 9.99,
        "category": "accessories",
        "inventory_count": 100,
        "image_url": "bike-light-1200x1500.37c843b0.jpg"
    },
    {
        "name": "Sauce Labs Bolt T-Shirt",
        "description": "Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.",
        "price": 15.99,
        "category": "clothing",
        "inventory_count": 75,
        "image_url": "bolt-shirt-1200x1500.c2599ac5.jpg"
    },
    {
        "name": "Sauce Labs Fleece Jacket",
        "description": "It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a relaxing day outdoors to a busy day at the office.",
        "price": 49.99,
        "category": "clothing",
        "inventory_count": 30,
        "image_url": "sauce-pullover-1200x1500.51d7ffaf.jpg"
    },
    {
        "name": "Sauce Labs Onesie",
        "description": "Rib snap infant onesie for the junior automation engineer in development. Reinforced 3-snap bottom closure, two-needle hemmed sleeved and bottom won't unravel.",
        "price": 7.99,
        "category": "clothing",
        "inventory_count": 60,
        "image_url": "red-onesie-1200x1500.2ec615b2.jpg"
    },
    {
        "name": "Test.allTheThings() T-Shirt (Red)",
        "description": "This classic Sauce Labs t-shirt is perfect to wear when cozying up to your keyboard to automate a few tests. Super-soft and comfy ringspun combed cotton.",
        "price": 15.99,
        "category": "clothing",
        "inventory_count": 80,
        "image_url": "red-tatt-1200x1500.30dadef4.jpg"
    }
]

# Sample users
USERS_DATA = [
    {
        "username": "standard_user",
        "email": "standard@example.com",
        "password": "pass123",
        "first_name": "Standard",
        "last_name": "User"
    },
    {
        "username": "problem_user",
        "email": "problem@example.com",
        "password": "pass123",
        "first_name": "Problem",
        "last_name": "User"
    },
    {
        "username": "performance_user",
        "email": "performance@example.com",
        "password": "pass123",
        "first_name": "Performance",
        "last_name": "User"
    }
]


def seed_database():
    """Seed database with initial data"""
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    #password_hasher = PasswordHasher()
    # Initialize the helper (it uses bcrypt by default)
    password_hasher = PasswordHash.recommended()  

    try:
        # Check if data already exists
        existing_products = db.query(Product).first()
        if existing_products:
            print("Database already seeded. Skipping...")
            return

        # Create users
        print("Creating users...")
        for user_data in USERS_DATA:
            #hashed_password = password_hasher.get_password_hash()
             # To hash a password
            hashed_password = password_hasher.hash(user_data["password"])
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hashed_password,
                first_name=user_data["first_name"],
                last_name=user_data["last_name"]
            )
            db.add(user)

        # Create products
        print("Creating products...")
        for product_data in PRODUCTS_DATA:
            product = Product(**product_data)
            db.add(product)

        db.commit()
        print("Database seeded successfully!")

        # Print user credentials
        print("\n" + "=" * 50)
        print("TEST USER CREDENTIALS")
        print("=" * 50)
        for user_data in USERS_DATA:
            print(f"Username: {user_data['username']}")
            print(f"Password: {user_data['password']}")
            print("-" * 50)

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
