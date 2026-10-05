from fastapi import APIRouter, Depends, UploadFile, File, Form, status, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.services.auth import get_current_user
from src.models import User, Photo

router = APIRouter(prefix="/photos", tags=["photos"])


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_photo(
    description: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    photo = Photo(
        url="https://res.cloudinary.com/demo/image/upload/sample.jpg",
        description=description,
        user_id=current_user.id,
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


@router.get("/search")
async def search_photos(
    keyword: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Photo)
    if keyword:
        query = query.filter(Photo.description.contains(keyword))
    return query.all()


@router.get("/{photo_id}")
async def get_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo