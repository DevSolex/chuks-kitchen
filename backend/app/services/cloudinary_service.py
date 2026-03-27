import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from app.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)

async def upload_image(file: UploadFile) -> str:
    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, or WebP images are allowed")
    contents = await file.read()
    result = cloudinary.uploader.upload(
        contents,
        folder="chuks_kitchen",
        transformation=[{"width": 800, "height": 600, "crop": "fill", "quality": "auto"}],
    )
    return result["secure_url"]
