from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from api.db.db import Base


class TransactionORM(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    comment = Column(String, nullable=True)
