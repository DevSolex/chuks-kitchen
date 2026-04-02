from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderItemOut(BaseModel):
    food_item_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True
