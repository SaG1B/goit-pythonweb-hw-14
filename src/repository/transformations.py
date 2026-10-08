from typing import Optional, List
from sqlalchemy.orm import Session
from src.models import Photo, User

def get_transformations(photo_id: int, db: Session) -> List[Photo]:
    return db.query(Photo).filter(Photo.id == photo_id).all()