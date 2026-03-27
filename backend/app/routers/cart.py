from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models.cart import CartItem
from app.models.food import FoodItem
from app.models.user import User
from app.schemas.cart import CartItemAdd, CartItemOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=List[CartItemOut])
def get_cart(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(CartItem).options(joinedload(CartItem.food_item)).filter(CartItem.user_id == user.id).all()

@router.post("/")
def add_to_cart(data: CartItemAdd, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    food = db.query(FoodItem).filter(FoodItem.id == data.food_item_id, FoodItem.available == True).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")
    existing = db.query(CartItem).filter(CartItem.user_id == user.id, CartItem.food_item_id == data.food_item_id).first()
    if existing:
        new_qty = existing.quantity + data.quantity
        if new_qty <= 0:
            db.delete(existing)
        else:
            existing.quantity = new_qty
    else:
        if data.quantity > 0:
            db.add(CartItem(user_id=user.id, food_item_id=data.food_item_id, quantity=data.quantity))
    db.commit()
    return {"message": "Cart updated"}

@router.delete("/{item_id}")
def remove_from_cart(item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item removed"}
