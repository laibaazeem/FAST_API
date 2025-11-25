from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "user"

    class Config:
        from_attributes = True

class LoginIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryOut(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: Optional[int] = 0

class ProductCreate(ProductBase):
    category_id: int
    total_units: int
    remaining_units: int
    quantity: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

class ProductOut(ProductBase):
    id: int
    category: CategoryOut
    stock_status: str
    quantity: Optional[int] = 0

    class Config:
        from_attributes = True


class CartProduct(BaseModel):
    product_id: int
    quantity: int

class CartCreate(BaseModel):
    user_id: int
    products: List[CartProduct]

class CartOut(BaseModel):
    id: int
    user_id: int
    created_at: Optional[datetime]
    products: List[ProductOut]

    class Config:
        from_attributes = True


class CheckoutOut(BaseModel):
    order_id: int
    user_id: int
    cart_id: int
    total_amount: float
    order_status: str
    order_time: Optional[str]

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id: int
    cart_id: int

class OrderOut(BaseModel):
    id: int
    user_id: int
    cart_id: int
    total_amount: float
    order_status: str
    order_time: Optional[str]
    user_email: Optional[str]

    class Config:
        from_attributes = True
