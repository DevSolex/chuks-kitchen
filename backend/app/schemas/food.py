from pydantic import BaseModel
from typing import Optional

class FoodItemOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    image_url: Optional[str]
    category: str
    available: bool

    class Config:
        from_attributes = True

class FoodItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str = "Main"
    available: bool = True
