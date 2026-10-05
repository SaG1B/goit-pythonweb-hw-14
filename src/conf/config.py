from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # База данных и JWT
    database_url: str = "sqlite:///./photoshare.db"
    secret_key: str = "supersecretkey1234567890"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Настройки Cloudinary
    cloudinary_name: str = "mpcmnmpr"
    cloudinary_api_key: str = "532189739322684"
    cloudinary_api_secret: str = "w0AplatQ33m76n7UauWDfo0cG4w"

    # Настройки почты (если используются)
    mail_username: str = "example@meta.ua"
    mail_password: str = "password"
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"

    # Настройки Redis (если используются)
    redis_host: str = "localhost"
    redis_port: int = 6379

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )


settings = Settings()