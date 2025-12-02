"""
Run this file to add sample categories and products to your database
Usage: python test_data.py
"""
import requests

API_BASE_URL = "http://127.0.0.1:8000"

# Sample Categories
categories = [
    {"name": "Electronics", "description": "Electronic devices and gadgets"},
    {"name": "Fashion", "description": "Clothing and accessories"},
    {"name": "Makeup", "description": "Cosmetics and beauty products"},
    {"name": "Books", "description": "Books and literature"}
]

# Sample Products
products = [
    {
        "name": "Laptop Pro",
        "description": "High-performance laptop for professionals",
        "price": 89999,
        "category_id": 1,  # Electronics
        "total_units": 50,
        "remaining_units": 50,
        "quantity": 50
    },
    {
        "name": "Smartphone X",
        "description": "Latest smartphone with advanced features",
        "price": 54999,
        "category_id": 1,
        "total_units": 100,
        "remaining_units": 100,
        "quantity": 100
    },
    {
        "name": "Wireless Headphones",
        "description": "Premium noise-cancelling headphones",
        "price": 8999,
        "category_id": 1,
        "total_units": 75,
        "remaining_units": 75,
        "quantity": 75
    },
    {
        "name": "Smart Watch",
        "description": "Fitness tracking smartwatch",
        "price": 15999,
        "category_id": 1,
        "total_units": 60,
        "remaining_units": 60,
        "quantity": 60
    },
    {
        "name": "T-Shirt",
        "description": "Comfortable cotton t-shirt",
        "price": 1499,
        "category_id": 2,  # Fashion
        "total_units": 200,
        "remaining_units": 200,
        "quantity": 200
    },
    {
        "name": "Jeans",
        "description": "Classic blue denim jeans",
        "price": 2999,
        "category_id": 2,
        "total_units": 150,
        "remaining_units": 150,
        "quantity": 150
    },
    {
        "name": "Running Shoes",
        "description": "Lightweight running shoes",
        "price": 4999,
        "category_id": 2,
        "total_units": 80,
        "remaining_units": 80,
        "quantity": 80
    },
    {
        "name": "Wrist Watch",
        "description": "Elegant analog wrist watch",
        "price": 3999,
        "category_id": 2,
        "total_units": 40,
        "remaining_units": 40,
        "quantity": 40
    }
]

def add_categories():
    print("Adding categories...")
    for cat in categories:
        try:
            response = requests.post(f"{API_BASE_URL}/categories/", json=cat)
            if response.status_code == 200:
                print(f"✅ Added category: {cat['name']}")
            else:
                print(f"❌ Failed to add {cat['name']}: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

def add_products():
    print("\nAdding products...")
    for prod in products:
        try:
            response = requests.post(f"{API_BASE_URL}/products/", json=prod)
            if response.status_code == 200:
                print(f"✅ Added product: {prod['name']}")
            else:
                print(f"❌ Failed to add {prod['name']}: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting to populate database...\n")
    add_categories()
    add_products()
    print("\n✅ Database population complete!")