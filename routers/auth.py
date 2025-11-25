from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas, models
from passlib.context import CryptContext
import jwt
import os
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "secret123")
ALGORITHM = "HS256"


def hash_password(password: str):

    if not password:
        raise HTTPException(status_code=400, detail="Password cannot be empty")
    password_bytes = password.encode("utf-8")[:72]  
    return pwd_context.hash(password_bytes)


def verify_password(password: str, hashed: str):
    if not password:
        return False
    password_bytes = password.encode("utf-8")[:72]  
    return pwd_context.verify(password_bytes, hashed)


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register_user(payload: schemas.RegisterIn, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(payload.password)
    user = models.User(email=payload.email, password_hash=hashed_pw, role=payload.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}


@router.post("/login", response_model=schemas.TokenOut)
def login_user(payload: schemas.LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
