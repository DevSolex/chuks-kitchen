from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.cart import CartItem
from app.models.food import FoodItem
from app.models.order import Order, OrderItem
from app.models.user import User
from app.schemas.order import OrderOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut)
def place_order(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0.0
    order = Order(user_id=user.id, total_price=0)
    db.add(order)
    db.flush()

    for ci in cart_items:
        food = db.query(FoodItem).filter(FoodItem.id == ci.food_item_id).first()
        total += food.price * ci.quantity
        db.add(OrderItem(order_id=order.id, food_item_id=food.id, quantity=ci.quantity, unit_price=food.price))

    order.total_price = total
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == user.id).order_by(Order.created_at.desc()).all()

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
