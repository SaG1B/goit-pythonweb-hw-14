from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


# Схеми для тегів
class TagModel(BaseModel):
    name: str = Field(max_length=50)

    model_config = ConfigDict(from_attributes=True)


class TagResponse(TagModel):
    id: int


# Схеми для опису світлини та оновлення
class PhotoUpdate(BaseModel):
    description: Optional[str] = Field(None, max_length=500)


# Основні схеми відповідей API для світлин
class PhotoResponse(BaseModel):
    id: int
    url: str
    public_id: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    user_id: int
    tags: List[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)


# Схема відповіді для трансформованих зображень з QR-кодом
class TransformedImageResponse(BaseModel):
    id: int
    url: str
    qr_code_url: Optional[str]
    created_at: datetime
    photo_id: int

    model_config = ConfigDict(from_attributes=True)


# Схема запиту на трансформацію
class TransformRequest(BaseModel):
    width: Optional[int] = Field(500, ge=10, le=2000)
    height: Optional[int] = Field(500, ge=10, le=2000)
    crop: Optional[str] = Field("fill", description="Режим кропу: fill, fit, crop, scale, pad")