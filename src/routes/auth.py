from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.user import UserModel, UserResponse, TokenModel
from src.repository import users as repository_users
from src.services.auth import (
    auth_service,
    get_password_hash,
    verify_password,
    create_access_token,
    BLACK_LIST,
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, db: Session = Depends(get_db)):
    exist_user = repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account with this email already exists"
        )
    body.password = get_password_hash(body.password)
    new_user = repository_users.create_user(body, db)
    return new_user

@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = repository_users.get_user_by_email(body.username, db)
    if user is None:
        from src.models import User
        user = db.query(User).filter(User.username == body.username).first()

    if user is None or not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(token: str = Depends(auth_service.oauth2_scheme)):
    BLACK_LIST.add(token)
    return {"message": "Successfully logged out"}