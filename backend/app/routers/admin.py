from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.user import User
from app.schemas.order import OrderOut
from app.schemas.user import UserOut
from app.dependencies import get_admin_user
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin"])

class StatusUpdate(BaseModel):
    status: str

@router.get("/orders", response_model=List[OrderOut])
def all_orders(db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    for o in orders:
        o.items = db.query(OrderItem).filter(OrderItem.order_id == o.id).all()
    return orders

@router.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = data.status
    db.commit()
    return {"message": "Status updated"}

@router.get("/users", response_model=List[UserOut])
def all_users(db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    return db.query(User).all()
