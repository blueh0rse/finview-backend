from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Asset(BaseModel):
    symbol: str
    name: str
    category: str
    current_price: float | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class AssetCreate(BaseModel):
    symbol: str
    name: str
    category: str
    current_price: float | None = None
    updated_at: datetime | None = None
