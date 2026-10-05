import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import HTTPException, status, UploadFile

# Налаштування Cloudinary з конфігурації оточення (.env)
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


def upload_image(file: UploadFile, folder: str = "photoshare") -> dict:
    """Завантажує фотографію в Cloudinary та повертає url і public_id."""
    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder=folder,
            resource_type="image",
        )
        return {
            "url": result.get("secure_url"),
            "public_id": result.get("public_id"),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка завантаження файлу в Cloudinary: {str(e)}",
        )


def delete_image(public_id: str) -> bool:
    """Видаляє фотографію з Cloudinary за її public_id."""
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result.get("result") == "ok"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка видалення файлу з Cloudinary: {str(e)}",
        )