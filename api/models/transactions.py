from typing import Literal
import uuid
from pydantic import BaseModel
from datetime import datetime


class Transaction(BaseModel):
    id: uuid.UUID
    asset_symbol: str
    operation: Literal["buy", "sell"]
    amount: float
    quantity: float
    unit_price: float
    currency: str
    date: datetime
    comment: str | None = None

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    asset_symbol: str
    operation: Literal["buy", "sell"]
    amount: float
    quantity: float
    unit_price: float
    currency: str
    date: datetime
    comment: str | None = None

    class Config:
        from_attributes = True


class TransactionUpdate(BaseModel):
    asset_symbol: str | None = None
    operation: Literal["buy", "sell"] | None = None
    amount: float | None = None
    quantity: float | None = None
    unit_price: float | None = None
    currency: str | None = None
    date: datetime | None = None
    comment: str | None = None

    class Config:
        from_attributes = True
