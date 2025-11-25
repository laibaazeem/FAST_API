from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas, models

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=schemas.OrderOut)
def make_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).get(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(models.Cart).get(payload.cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    total = sum(item.product.price * item.quantity for item in cart.items)
    for item in cart.items:
        if item.product.remaining_units < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {item.product.name}. Only {item.product.remaining_units} left."
            )
        item.product.remaining_units -= item.quantity

    # order = models.Order(user_id=user.id, cart_id=cart.id, total_amount=total, order_status="pending")
    # db.add(order)
    # db.commit()
    # db.refresh(order)

    # Create a new cart for this order
    order_cart = models.Cart(user_id=user.id)
    db.add(order_cart)
    db.commit()
    db.refresh(order_cart)

    # Copy items from the original cart
    for item in cart.items:
        order_item = models.CartItem(
            cart_id=order_cart.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)
    db.commit()

    # Create the order linked to the new cart
    order = models.Order(
        user_id=user.id,
        cart_id=order_cart.id,
        total_amount=total,
        order_status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)


    return {
        "id": order.id,
        "user_id": order.user_id,
        "cart_id": order.cart_id,
        "total_amount": order.total_amount,
        "order_status": order.order_status,
        "order_time": order.order_time.isoformat() if order.order_time else None,
        "user_email": user.email
    }


@router.get("/", response_model=list[schemas.OrderOut])
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).order_by(models.Order.order_time.desc()).all()
    result = []
    for o in orders:
        result.append({
            "id": o.id,
            "user_id": o.user_id,
            "cart_id": o.cart_id,
            "total_amount": o.total_amount,
            "order_status": o.order_status,
            "order_time": o.order_time.isoformat() if o.order_time else None,
            "user_email": o.user.email
        })
    return result


@router.get("/details/{user_id}")
def get_order_details(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    orders = db.query(models.Order).filter(models.Order.user_id == user_id).order_by(models.Order.order_time.desc()).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")

    detailed_orders = []
    for o in orders:
        products = [
            {"id": ci.product.id, "name": ci.product.name, "price": ci.product.price, "quantity": ci.quantity}
            for ci in o.cart.items
        ]
        detailed_orders.append({
            "order_id": o.id,
            "cart_id": o.cart_id,
            "total_amount": o.total_amount,
            "order_status": o.order_status,
            "order_time": o.order_time,
            "products": products
        })
    return detailed_orders
