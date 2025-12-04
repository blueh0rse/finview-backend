from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from api.db.db import Base
import enum


class OperationEnum(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"


class CurrencyEnum(str, enum.Enum):
    EUR = "EUR"
    USD = "USD"


class TransactionORM(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_symbol = Column(
        String, ForeignKey("assets.symbol", ondelete="CASCADE"), nullable=False
    )
    operation = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now)
    comment = Column(String, nullable=True)

    asset = relationship("AssetORM", back_populates="transactions")
