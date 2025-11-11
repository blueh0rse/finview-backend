from sqlalchemy import func
from api.db.db import SessionLocal
from api.schemas.transactions import OperationEnum, TransactionORM

MAX_TRANSACTIONS = 100


async def get_portefolio_value() -> float:
    print("[PORTEFOLIO] CALC VALUE")
    db = SessionLocal()
    try:
        buy_total = (
            db.query(func.sum(TransactionORM.amount))
            .filter(TransactionORM.operation == OperationEnum.BUY.value)
            .scalar()
            or 0
        )
        sell_total = (
            db.query(func.sum(TransactionORM.amount))
            .filter(TransactionORM.operation == OperationEnum.SELL.value)
            .scalar()
            or 0
        )

        total_value = buy_total - sell_total
        return float(total_value)
    finally:
        db.close()
