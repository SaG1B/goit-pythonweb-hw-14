from typing import Optional, List
from sqlalchemy.orm import Session
from src.models import Photo, User
from src.schemas.photo import PhotoUpdate

def create_photo(
    db: Session, 
    url: str, 
    description: Optional[str], 
    user: User, 
    public_id: Optional[str] = None
) -> Photo:
    photo_kwargs = {
        "url": url,
        "description": description,
        "user_id": user.id
    }
    
    if hasattr(Photo, "public_id") and public_id is not None:
        photo_kwargs["public_id"] = public_id

    photo = Photo(**photo_kwargs)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

def get_photos(skip: int, limit: int, db: Session) -> List[Photo]:
    return db.query(Photo).offset(skip).limit(limit).all()

def get_photo_by_id(photo_id: int, db: Session) -> Optional[Photo]:
    return db.query(Photo).filter(Photo.id == photo_id).first()

def update_photo(photo_id: int, body: PhotoUpdate, db: Session, user: User) -> Optional[Photo]:
    photo = db.query(Photo).filter(Photo.id == photo_id, Photo.user_id == user.id).first()
    if photo:
        if body.description is not None:
            photo.description = body.description
        db.commit()
        db.refresh(photo)
    return photo

def delete_photo(photo_id: int, db: Session, user: User) -> Optional[Photo]:
    photo = db.query(Photo).filter(Photo.id == photo_id, Photo.user_id == user.id).first()
    if photo:
        db.delete(photo)
        db.commit()
    return photo