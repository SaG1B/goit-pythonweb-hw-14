from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import Optional

from src.database.db import get_db
from src.models import User, Photo, Role
from src.services.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


# Схема для оновлення власного профілю
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


@router.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Отримання власного профілю користувача"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role),
        "is_banned": getattr(current_user, "is_banned", False),
        "created_at": getattr(current_user, "created_at", None),
    }


@router.put("/me")
def update_my_profile(
    body: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Редагування власної інформації користувача"""
    if body.username:
        existing_user = db.query(User).filter(User.username == body.username, User.id != current_user.id).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
        current_user.username = body.username

    if body.email:
        existing_email = db.query(User).filter(User.email == body.email, User.id != current_user.id).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken")
        current_user.email = body.email

    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/{username}")
def get_user_profile(
    username: str,
    db: Session = Depends(get_db),
):
    """Публічний профіль користувача за його унікальним юзернеймом (без авторизації)"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    photos_count = db.query(Photo).filter(Photo.user_id == user.id).count()

    return {
        "id": user.id,
        "username": user.username,
        "created_at": getattr(user, "created_at", None),
        "photos_count": photos_count,
    }


@router.patch("/{user_id}/ban")
def ban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Адміністратор робить користувача неактивним (забаненим)"""
    user_role = current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role)
    if user_role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can ban users",
        )

    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    target_user.is_banned = True
    db.commit()
    return {"message": f"User {target_user.username} has been banned"}