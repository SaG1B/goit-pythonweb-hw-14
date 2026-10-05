from pydantic import BaseModel, EmailStr
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Role

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str