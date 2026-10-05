from typing import Optional, List
from sqlalchemy.orm import Session
from src.models.photo import TransformedImage


def create_transformed_image(
    db: Session, photo_id: int, url: str, qr_code_url: Optional[str]
) -> TransformedImage:
    """Зберігає трансформоване зображення та посилання на QR-код у БД."""
    transformed_image = TransformedImage(
        photo_id=photo_id,
        url=url,
        qr_code_url=qr_code_url
    )
    db.add(transformed_image)
    db.commit()
    db.refresh(transformed_image)
    return transformed_image


def get_transformed_images_for_photo(db: Session, photo_id: int) -> List[TransformedImage]:
    """Отримує всі трансформовані версії для конкретної світлини."""
    return db.query(TransformedImage).filter(TransformedImage.photo_id == photo_id).all()