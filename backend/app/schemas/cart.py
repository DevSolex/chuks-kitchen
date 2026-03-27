from pydantic import BaseModel
from app.schemas.food import FoodItemOut

class CartItemAdd(BaseModel):
    food_item_id: int
    quantity: int = 1

class CartItemOut(BaseModel):
    id: int
    food_item: FoodItemOut
    quantity: int

    class Config:
        from_attributes = True
