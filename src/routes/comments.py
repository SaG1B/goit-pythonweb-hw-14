from datetime import datetime
from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.models import Comment, Photo, Role, User
from src.services.auth import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/photo/{photo_id}", status_code=status.HTTP_201_CREATED)
def create_comment(
    photo_id: int,
    text: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )

    comment = Comment(text=text, user_id=current_user.id, photo_id=photo_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.put("/{comment_id}")
def update_comment(
    comment_id: int,
    text: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own comments",
        )

    comment.text = text
    comment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    # Перевіряємо роль користувача (ADMIN або MODERATOR)
    user_role = (
        current_user.role.value
        if hasattr(current_user.role, "value")
        else str(current_user.role)
    )

    if user_role.lower() not in ["admin", "moderator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators and moderators can delete comments",
        )

    db.delete(comment)
    db.commit()
    return None