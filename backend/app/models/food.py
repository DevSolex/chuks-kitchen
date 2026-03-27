from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from app.database import Base

class FoodItem(Base):
    __tablename__ = "food_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String(500))
    category = Column(String(100), default="Main")
    available = Column(Boolean, default=True)
