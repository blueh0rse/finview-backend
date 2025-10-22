from datetime import datetime
from typing import List
import uuid
from api.models.transactions import Transaction


async def get_all_transactions() -> List[Transaction]:
    print("[LOG] SERVICE: get_all_transactions")
    transactions = [
        Transaction(
            id=uuid.uuid4(),
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
    return transactions
