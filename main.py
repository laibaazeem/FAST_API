from fastapi import FastAPI
from database import engine, Base
import routers.auth as auth
import routers.category as category
import routers.products as products
import routers.cart as cart
import routers.orders as orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce API (ORM Version)")


app.include_router(auth.router)
app.include_router(category.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)


