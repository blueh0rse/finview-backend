from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import relationship
from api.db.db import Base


class AssetORM(Base):
    __tablename__ = "assets"

    symbol = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    current_price = Column(Float, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    transactions = relationship(
        "TransactionORM", back_populates="asset", cascade="all, delete-orphan"
    )
