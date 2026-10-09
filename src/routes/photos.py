from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.models import User
from src.schemas.photo import PhotoResponse, PhotoUpdate
from src.repository import photos as repository_photos
from src.services.auth import auth_service
from src.conf.config import settings

router = APIRouter(prefix="/photos", tags=["photos"])

cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)

@router.post("/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
async def create_photo(
    description: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    photo: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    upload_file = file or photo or image
    if not upload_file:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="File is required"
        )

    try:
        upload_result = cloudinary.uploader.upload(
            upload_file.file, 
            folder="photoshare"
        )
        photo_url = upload_result.get("secure_url")
        public_id = upload_result.get("public_id")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Cloudinary upload error: {str(e)}"
        )

    return repository_photos.create_photo(
        db=db, 
        url=photo_url, 
        description=description, 
        user=current_user,
        public_id=public_id
    )

@router.get("/", response_model=List[PhotoResponse])
async def read_photos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository_photos.get_photos(skip=skip, limit=limit, db=db)

@router.get("/{photo_id}", response_model=PhotoResponse)
async def read_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = repository_photos.get_photo_by_id(photo_id, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo

@router.put("/{photo_id}", response_model=PhotoResponse)
async def update_photo(
    photo_id: int,
    body: PhotoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    photo = repository_photos.update_photo(photo_id, body, db, current_user)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found or operation not permitted")
    return photo

@router.delete("/{photo_id}", response_model=PhotoResponse)
async def delete_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    photo = repository_photos.delete_photo(photo_id, db, current_user)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found or operation not permitted")
    return photo