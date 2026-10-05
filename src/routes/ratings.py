from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database.db import get_db
from src.models import Rating, Photo, User
from src.services.auth import get_current_user

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.post("/photo/{photo_id}", status_code=status.HTTP_201_CREATED)
def create_rating(
    photo_id: int,
    value: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Виставити рейтинг світлині від 1 до 5 зірок"""
    if value < 1 or value > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5",
        )

    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )

    # 1. Неможливо оцінювати свої світлини
    if photo.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot rate your own photo",
        )

    # 2. Можна тільки раз виставляти оцінку світлині
    existing_rating = (
        db.query(Rating)
        .filter(Rating.photo_id == photo_id, Rating.user_id == current_user.id)
        .first()
    )
    if existing_rating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already rated this photo",
        )

    rating = Rating(value=value, photo_id=photo_id, user_id=current_user.id)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


@router.get("/photo/{photo_id}")
def get_photo_rating(photo_id: int, db: Session = Depends(get_db)):
    """Отримати середній рейтинг світлини"""
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )

    avg_rating = (
        db.query(func.avg(Rating.value)).filter(Rating.photo_id == photo_id).scalar()
    )
    total_votes = db.query(Rating).filter(Rating.photo_id == photo_id).count()

    return {
        "photo_id": photo_id,
        "average_rating": round(avg_rating, 2) if avg_rating else 0.0,
        "total_votes": total_votes,
    }


@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(
    rating_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Модератори та адміністратори можуть видаляти оцінки"""
    user_role = (
        current_user.role.value
        if hasattr(current_user.role, "value")
        else str(current_user.role)
    )
    if user_role.lower() not in ["admin", "moderator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators and moderators can delete ratings",
        )

    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found"
        )

    db.delete(rating)
    db.commit()
    return None