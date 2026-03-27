from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_item_id = Column(Integer, ForeignKey("food_items.id"), nullable=False)
    quantity = Column(Integer, default=1)

    food_item = relationship("FoodItem", lazy="joined")
