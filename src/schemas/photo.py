from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class PhotoModel(BaseModel):
    description: Optional[str] = None


class PhotoResponse(BaseModel):
    id: int
    url: str
    description: Optional[str] = None
    public_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# Псевдоніми для забезпечення сумісності з тестами та різними роутерами
PhotoCreate = PhotoModel
PhotoUpdate = PhotoModel
PhotoSchema = PhotoResponse