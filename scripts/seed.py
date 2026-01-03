import asyncio
import sys
import os
from sqlalchemy import select

# Add project root to path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.core.database import async_session
from api.src.users.models import User
from api.src.goods.models import Goods
from api.src.orders.models import OrderInfo, OrderItem
from api.core.security import get_password_hash

async def seed_data():
    """Seed the database with initial data."""
    async with async_session() as session:
        try:
            print("Starting database seed...")

            # 1. Create Users
            print("Checking/Creating Users...")
            # Admin User
            result = await session.execute(select(User).where(User.email == "admin@example.com"))
            if not result.scalar_one_or_none():
                admin = User(
                    email="admin@example.com",
                    hashed_password=get_password_hash("admin123")
                )
                session.add(admin)
                print("  - Created admin user (admin@example.com / admin123)")
            else:
                print("  - Admin user already exists")

            # Normal User
            result = await session.execute(select(User).where(User.email == "user@example.com"))
            user = result.scalar_one_or_none()
            if not user:
                user = User(
                    email="user@example.com",
                    hashed_password=get_password_hash("user123")
                )
                session.add(user)
                print("  - Created normal user (user@example.com / user123)")
            else:
                print("  - Normal user already exists")
            
            await session.flush() # Flush to get IDs
            
            # Refresh user to ensure we have the ID (especially if it was just added)
            if user is None: # Should not happen if logic above is correct, but for safety
                 result = await session.execute(select(User).where(User.email == "user@example.com"))
                 user = result.scalar_one()

            # 2. Create Goods
            print("Checking/Creating Goods...")
            goods_list = [
                {
                    "name": "iPhone 15", 
                    "title": "Apple iPhone 15 Pro Max 256GB", 
                    "price": 999.00, 
                    "stock": 100, 
                    "img": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15-pro-max.jpg", 
                    "detail": "The iPhone 15 Pro Max display has rounded corners that follow a beautiful curved design, and these corners are within a standard rectangle."
                },
                {
                    "name": "MacBook Pro", 
                    "title": "Apple MacBook Pro 14 M3", 
                    "price": 1999.00, 
                    "stock": 50, 
                    "img": "https://fdn2.gsmarena.com/vv/bigpic/apple-macbook-pro-14-2023.jpg", 
                    "detail": "MacBook Pro blasts forward with the M3, M3 Pro, and M3 Max chips."
                },
                {
                    "name": "AirPods Pro", 
                    "title": "Apple AirPods Pro (2nd generation)", 
                    "price": 249.00, 
                    "stock": 200, 
                    "img": "https://fdn2.gsmarena.com/vv/bigpic/apple-airpods-pro-2.jpg", 
                    "detail": "AirPods Pro feature up to 2x more Active Noise Cancellation, plus Adaptive Transparency, and Personalized Spatial Audio."
                },
            ]
            
            created_goods = []
            for item in goods_list:
                result = await session.execute(select(Goods).where(Goods.name == item["name"]))
                existing = result.scalar_one_or_none()
                if not existing:
                    new_good = Goods(**item)
                    session.add(new_good)
                    created_goods.append(new_good)
                    print(f"  - Created good: {item['name']}")
                else:
                    created_goods.append(existing)
                    print(f"  - Good already exists: {item['name']}")
            
            await session.flush()

            # 3. Create Orders (for the normal user)
            print("Checking/Creating Orders...")
            # Check if user has any orders
            result = await session.execute(select(OrderInfo).where(OrderInfo.user_id == user.id))
            if not result.first():
                # We need at least 2 goods to create the sample order
                if len(created_goods) >= 2:
                    good1 = created_goods[0] # iPhone
                    good2 = created_goods[2] # AirPods
                    
                    total_amount = float(good1.price) + float(good2.price)
                    
                    # Create an order
                    order = OrderInfo(
                        user_id=user.id,
                        delivery_addr_id=1, # Dummy address ID
                        total_amount=total_amount,
                        status=1, # 1 typically means paid/confirmed in many systems, or just 'created'
                        order_type=0
                    )
                    session.add(order)
                    await session.flush()
                    
                    # Add items to order
                    item1 = OrderItem(
                        order_id=order.id,
                        goods_id=good1.id,
                        goods_name=good1.name,
                        goods_price=good1.price,
                        count=1,
                        item_amount=good1.price
                    )
                    item2 = OrderItem(
                        order_id=order.id,
                        goods_id=good2.id,
                        goods_name=good2.name,
                        goods_price=good2.price,
                        count=1,
                        item_amount=good2.price
                    )
                    session.add(item1)
                    session.add(item2)
                    print(f"  - Created sample order for user {user.email}")
                else:
                     print("  - Not enough goods to create sample order")
            else:
                print(f"  - Orders already exist for user {user.email}")

            await session.commit()
            print("Seeding completed successfully!")
            
        except Exception as e:
            print(f"An error occurred during seeding: {e}")
            await session.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(seed_data())
