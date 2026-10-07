import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    sqlalchemy_database_url: str = "sqlite:///./photoshare.db"
    secret_key: str = "secret_key_change_me"
    algorithm: str = "HS256"
    cloudinary_name: str = "demo"
    cloudinary_api_key: str = "1234567890"
    cloudinary_api_secret: str = "secret"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()