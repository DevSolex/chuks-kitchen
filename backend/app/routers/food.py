from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.food import FoodItem
from app.schemas.food import FoodItemOut
from app.services.cloudinary_service import upload_image
from app.dependencies import get_admin_user

router = APIRouter(prefix="/food", tags=["Food"])

@router.get("/", response_model=List[FoodItemOut])
def list_food(category: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(FoodItem).filter(FoodItem.available == True)
    if category:
        q = q.filter(FoodItem.category == category)
    return q.all()

@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    rows = db.query(FoodItem.category).distinct().all()
    return [r[0] for r in rows]

@router.post("/", response_model=FoodItemOut)
async def add_food(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    category: str = Form("Main"),
    available: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    _: object = Depends(get_admin_user),
):
    image_url = await upload_image(image) if image and image.filename else None
    item = FoodItem(name=name, description=description, price=price,
                    category=category, available=available, image_url=image_url)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.patch("/{item_id}", response_model=FoodItemOut)
async def update_food(
    item_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    category: Optional[str] = Form(None),
    available: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    _: object = Depends(get_admin_user),
):
    item = db.query(FoodItem).filter(FoodItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Food item not found")
    if name: item.name = name
    if description: item.description = description
    if price: item.price = price
    if category: item.category = category
    if available is not None: item.available = available
    if image and image.filename:
        item.image_url = await upload_image(image)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_food(item_id: int, db: Session = Depends(get_db), _: object = Depends(get_admin_user)):
    item = db.query(FoodItem).filter(FoodItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Food item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted"}
