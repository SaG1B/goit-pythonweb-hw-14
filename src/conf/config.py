import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    sqlalchemy_database_url: str = "sqlite:///./test.db"
    secret_key: str = "secret"
    algorithm: str = "HS256"
    mail_username: str = "example@example.com"
    mail_password: str = "password"
    mail_from: str = "example@example.com"
    mail_port: int = 587
    mail_server: str = "smtp.example.com"
    redis_host: str = "localhost"
    redis_port: int = 6379
    cloudinary_name: str = "demo"
    cloudinary_api_key: str = "123456789"
    cloudinary_api_secret: str = "secret"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def __init__(self, **values):
        super().__init__(**values)
        env_db_url = os.getenv("DATABASE_URL")
        if env_db_url:
            self.sqlalchemy_database_url = env_db_url

settings = Settings()