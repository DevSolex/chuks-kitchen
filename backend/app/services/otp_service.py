import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.otp import OTP
from app.config import settings

def generate_otp(user_id: int, db: Session) -> str:
    code = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    db.query(OTP).filter(OTP.user_id == user_id, OTP.used == False).delete()
    otp = OTP(user_id=user_id, code=code, expires_at=expires_at)
    db.add(otp)
    db.commit()
    # In production: send via email/SMS. For now, return it directly.
    return code

def verify_otp(user_id: int, code: str, db: Session) -> bool:
    otp = db.query(OTP).filter(
        OTP.user_id == user_id,
        OTP.code == code,
        OTP.used == False,
        OTP.expires_at > datetime.utcnow()
    ).first()
    if not otp:
        return False
    otp.used = True
    db.commit()
    return True
