from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    OTP_EXPIRE_MINUTES: int = 10

    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()
