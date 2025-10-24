from datetime import datetime
from typing import List
import uuid
from api.db.db import SessionLocal
from api.models.transactions import Transaction
from api.schemas.transactions import TransactionORM

transactions = [
    Transaction(
        id=uuid.UUID('16fd2706-8baf-433b-82eb-8c7fada847da'),
        asset="BTC",
        operation="buy",
        amount=500.0,
        quantity=0.01,
        unit_price=50000.0,
        currency="EUR",
        date=datetime(2024, 10, 1, 14, 30),
        comment="First BTC buy",
    ),
    Transaction(
        id=uuid.uuid4(),
        asset="ETH",
        operation="buy",
        amount=300.0,
        quantity=0.1,
        unit_price=3000.0,
        currency="EUR",
        date=datetime(2024, 10, 3, 10, 0),
        comment="ETH position",
    ),
    Transaction(
        id=uuid.uuid4(),
        asset="BTC",
        operation="sell",
        amount=250.0,
        quantity=0.005,
        unit_price=50000.0,
        currency="EUR",
        date=datetime(2024, 10, 10, 16, 45),
        comment="Partial BTC sale",
    ),
]


async def get_all_transactions() -> List[Transaction]:
    print("[LOG] SERVICE: get_all_transactions")
    db = SessionLocal()
    try:
        transactions = db.query(TransactionORM).all()
        return [Transaction.model_validate(tx) for tx in transactions]
    finally:
        db.close()


async def get_transaction_by_id(transaction_id: uuid.UUID) -> Transaction:
    print(f"[LOG] SERVICE: get_transaction_by_id {transaction_id}")
    for tx in transactions:
        if tx.id == transaction_id:
            return tx
    return None
