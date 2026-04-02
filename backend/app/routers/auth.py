from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, OTPVerify, TokenResponse, UserOut
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.services.otp_service import generate_otp, verify_otp
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(name=data.name, email=data.email, hashed_password=hash_password(data.password), is_verified=True)
    db.add(user)
    db.commit()
    return {"message": "Registration successful. You can now log in."}

@router.post("/verify-otp")
def verify(data: OTPVerify, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_otp(user.id, data.code, db):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    user.is_verified = True
    db.commit()
    return {"message": "Account verified successfully"}

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Account not verified")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
