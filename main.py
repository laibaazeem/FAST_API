from fastapi import FastAPI
from database import engine, Base
import routers.auth as auth
import routers.category as category
import routers.products as products
import routers.cart as cart
import routers.orders as orders
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce API (ORM Version)")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML templates
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(category.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)

# ===== ALL PAGE ROUTES =====

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/products")
def products_page(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})

@app.get("/categories")
def categories_page(request: Request):
    return templates.TemplateResponse("categories.html", {"request": request})

@app.get("/search")
def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.get("/cart")
def cart_page(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})