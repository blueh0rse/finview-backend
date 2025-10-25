import uuid
from pydantic import BaseModel
from datetime import datetime


class Transaction(BaseModel):
    id: uuid.UUID
    asset: str
    operation: str
    amount: float
    quantity: float
    unit_price: float
    currency: str
    date: datetime
    comment: str | None = None

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    asset: str
    operation: str
    amount: float
    quantity: float
    unit_price: float
    currency: str
    date: datetime
    comment: str | None = None
