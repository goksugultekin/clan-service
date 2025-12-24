from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

ALLOWED = {"TR", "US", "UK", "DE", "FR", "JP", "BR", "RU"}

class ClanCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    region: str = Field(..., description="Region code, e.g. TR, US, JP")
    description: Optional[str] = ""


class ClanOut(BaseModel):
    id: UUID
    name: str
    region: str
    description: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
