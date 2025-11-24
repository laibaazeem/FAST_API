# main.py
from fastapi import FastAPI
from database import engine, Base
import routers.auth as auth
import routers.category as category
import routers.products as products
import routers.cart as cart
import routers.orders as orders

# Automatically create all tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce API (ORM Version)")

# Include all routers
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Welcome to the E-commerce API with SQLAlchemy ORM!"}
