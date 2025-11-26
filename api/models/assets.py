from pydantic import BaseModel
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


class AssetUpdate(BaseModel):
    symbol: str | None = None
    name: str | None = None
    category: str | None = None
    current_price: float | None = None
    updated_at: datetime | None = None
