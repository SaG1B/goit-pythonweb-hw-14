from typing import List, Optional
from sqlalchemy.orm import Session

from src.models.photo import Photo, Tag
from src.models.user import User


def get_or_create_tags(db: Session, tag_names: List[str]) -> List[Tag]:
    """Знаходить існуючі теги або створює нові."""
    tags = []
    for name in tag_names:
        clean_name = name.lower().strip()
        if not clean_name:
            continue
        tag = db.query(Tag).filter(Tag.name == clean_name).first()
        if not tag:
            tag = Tag(name=clean_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tags.append(tag)
    return tags


def create_photo(
    db: Session,
    url: str,
    public_id: str,
    description: Optional[str],
    tags: List[Tag],
    user: User,
) -> Photo:
    """Створює новий запис світлини у БД."""
    photo = Photo(
        url=url,
        public_id=public_id,
        description=description,
        tags=tags,
        user_id=user.id,
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


def get_photo_by_id(db: Session, photo_id: int) -> Optional[Photo]:
    """Отримує світлину за її ID."""
    return db.query(Photo).filter(Photo.id == photo_id).first()


def update_photo_description(
    db: Session, photo_id: int, description: Optional[str], user: User
) -> Optional[Photo]:
    """Оновлює опис світлини."""
    photo = get_photo_by_id(db, photo_id)
    if photo:
        photo.description = description
        db.commit()
        db.refresh(photo)
    return photo


def delete_photo(db: Session, photo_id: int, user: User) -> Optional[Photo]:
    """Видаляє світлину з бази даних."""
    photo = get_photo_by_id(db, photo_id)
    if photo:
        db.delete(photo)
        db.commit()
    return photo