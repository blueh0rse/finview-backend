from typing import List
import uuid
from api.db.db import SessionLocal
from api.models.transactions import Transaction
from api.schemas.transactions import TransactionORM

MAX_TRANSACTIONS = 100


async def get_all_transactions(skip, limit) -> List[Transaction]:
    print("[TRANSACTION] GET ALL")
    if limit > MAX_TRANSACTIONS:
        limit = MAX_TRANSACTIONS
    db = SessionLocal()
    try:
        transactions = db.query(TransactionORM).offset(skip).limit(limit).all()
        return [Transaction.model_validate(tx) for tx in transactions]
    finally:
        db.close()


async def get_transaction_by_id(transaction_id: uuid.UUID) -> Transaction:
    print(f"[TRANSACTION] GET BY ID {transaction_id}")
    db = SessionLocal()
    try:
        tx = (
            db.query(TransactionORM).filter(TransactionORM.id == transaction_id).first()
        )
        if not tx:
            return False
        return Transaction.model_validate(tx)
    finally:
        db.close()


async def create_one_transaction(transaction: Transaction) -> Transaction:
    print(
        f"[TRANSACTION] CREATE {transaction.asset} - {transaction.operation} - {transaction.amount}{transaction.currency}"
    )
    db = SessionLocal()
    try:
        tx = TransactionORM(**transaction.model_dump())
        db.add(tx)
        db.commit()
        db.refresh(tx)
        return Transaction.model_validate(tx)
    except Exception as e:
        db.rollback()
        print("[ERROR] create_transaction:", e)
        raise
    finally:
        db.close()


async def update_one_transaction(transaction: Transaction) -> Transaction:
    print(f"[TRANSACTION] UPDATE {transaction.id}")
    db = SessionLocal()
    try:
        tx = (
            db.query(TransactionORM).filter(TransactionORM.id == transaction.id).first()
        )
        if not tx:
            return False
        for key, value in transaction.model_dump().items():
            setattr(tx, key, value)
        db.commit()
        db.refresh(tx)
        return Transaction.model_validate(tx)
    except Exception as e:
        db.rollback()
        print("[ERROR] update_transaction:", e)
        raise
    finally:
        db.close()


async def delete_one_transaction(transaction_id: uuid.UUID) -> bool:
    print(f"[TRANSACTION] DELETE {transaction_id}")
    db = SessionLocal()
    try:
        tx = (
            db.query(TransactionORM).filter(TransactionORM.id == transaction_id).first()
        )
        if not tx:
            return False
        db.delete(tx)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print("[ERROR] delete_transaction:", e)
        raise
    finally:
        db.close()
