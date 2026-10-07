from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class UserModel(BaseModel):
    username: str
    email: EmailStr
    password: str

# Псевдоніми для сумісності
UserSchema = UserModel
UserCreate = UserModel

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class TokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Псевдоніми для сумісності з тестами
Token = TokenModel
TokenResponse = TokenModel