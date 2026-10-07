from sqlalchemy.orm import Session
from src.models import User
from src.schemas.user import UserModel

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def create_user(body: UserModel, db: Session):
    user_kwargs = {
        "username": body.username,
        "email": body.email,
        "password": body.password,
    }
    
    # Додаємо додаткові поля тільки якщо вони визначені в моделі User
    if hasattr(User, "avatar"):
        user_kwargs["avatar"] = getattr(body, "avatar", None)
    if hasattr(User, "avatar_url"):
        user_kwargs["avatar_url"] = getattr(body, "avatar", None)
    if hasattr(User, "role"):
        user_kwargs["role"] = getattr(body, "role", "user")

    new_user = User(**user_kwargs)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user