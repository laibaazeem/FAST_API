# cart.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas, models

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/", response_model=schemas.CartOut)
def add_to_cart(payload: schemas.CartCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).get(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart = models.Cart(user_id=payload.user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)

    for item in payload.products:
        product = db.query(models.Product).get(item.product_id)
        if not product:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} not found")
        if product.remaining_units < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product.id}. Only {product.remaining_units} left."
            )
        cart_item = models.CartItem(cart_id=cart.id, product_id=product.id, quantity=item.quantity)
        db.add(cart_item)
    db.commit()

    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "created_at": cart.created_at,
        "products": [
            {"id": ci.product.id, "name": ci.product.name, "price": ci.product.price, "quantity": ci.quantity}
            for ci in cart.items
        ]
    }


@router.post("/checkout/{cart_id}", response_model=schemas.CheckoutOut)
def checkout_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).get(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    if cart.is_checked_out:
        raise HTTPException(status_code=400, detail="Cart already checked out")
    if not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    for item in cart.items:
        if item.product.remaining_units < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {item.product.name}. Only {item.product.remaining_units} left."
            )
        item.product.remaining_units -= item.quantity
        total += item.product.price * item.quantity

    order = models.Order(user_id=cart.user_id, cart_id=cart.id, total_amount=total, order_status="confirmed")
    cart.is_checked_out = True
    db.add(order)
    db.commit()
    db.refresh(order)

    return {
        "order_id": order.id,
        "user_id": order.user_id,
        "cart_id": order.cart_id,
        "total_amount": order.total_amount,
        "order_status": order.order_status,
        "order_time": order.order_time
    }


@router.get("/user/{user_id}", response_model=list[schemas.CartOut])
def get_cart_details(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    carts = db.query(models.Cart).filter(models.Cart.user_id == user_id).all()
    if not carts:
        raise HTTPException(status_code=404, detail="No carts found for this user")

    result = []
    for c in carts:
        result.append({
            "id": c.id,
            "user_id": c.user_id,
            "created_at": c.created_at,
            "products": [
                {"id": ci.product.id, "name": ci.product.name, "price": ci.product.price, "quantity": ci.quantity}
                for ci in c.items
            ]
        })
    return result
